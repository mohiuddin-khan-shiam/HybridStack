"""
HybridStack Ensemble Pipeline with Bayesian Optimization.

An implementation of the two-stage hybrid stacking ensemble framework combining
gradient-boosted trees (XGBoost) and regularized linear regression (Ridge).
"""

import os
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from skopt import gp_minimize
from skopt.space import Integer, Real
from skopt.utils import use_named_args
import joblib


def rmse_from_arrays(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculates the root mean squared error between two arrays."""
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


class HybridStackPipeline:
    """Pipeline class for optimizing and training the HybridStack model."""

    def __init__(self, n_splits: int = 5, seed: int = 42):
        self.seed = seed
        self.kf = KFold(n_splits=n_splits, shuffle=False)
        
        # Define hyperparameter spaces for optimization
        self.xgb_space = [
            Integer(3, 12, name="max_depth"),
            Real(0.01, 0.3, prior="log-uniform", name="learning_rate"),
            Integer(200, 2000, name="n_estimators"),
            Real(0.6, 1.0, name="subsample"),
            Real(0.6, 1.0, name="colsample_bytree"),
            Real(0.0, 10.0, name="reg_lambda"),
            Real(0.0, 5.0, name="reg_alpha"),
            Integer(64, 1024, name="max_bin"),
            Integer(1, 64, name="min_child_weight")
        ]
        
        self.ridge_space = [Real(1e-4, 1e4, prior="log-uniform", name="alpha")]
        
        self.xgb_base_params = {
            "objective": "reg:squarederror",
            "eval_metric": "rmse",
            "tree_method": "hist",
            "device": "cpu",  # Configured to CPU for general-purpose execution
            "seed": self.seed
        }
        
        self.xgb_best: Dict[str, Any] = {}
        self.ridge_best_alpha: float = 1.0
        self.meta_model: Any = None

    def optimize_hyperparameters(self, X_train: pd.DataFrame, y_train: pd.Series, 
                               xgb_calls: int = 35, ridge_calls: int = 25) -> Tuple[Dict[str, Any], float]:
        """Runs Bayesian optimization to locate optimal parameters for both base learners."""
        
        @use_named_args(self.xgb_space)
        def xgb_cv_objective(**params):
            p = self.xgb_base_params.copy()
            p.update({
                "max_depth": int(params["max_depth"]),
                "learning_rate": float(params["learning_rate"]),
                "subsample": float(params["subsample"]),
                "colsample_bytree": float(params["colsample_bytree"]),
                "reg_lambda": float(params["reg_lambda"]),
                "reg_alpha": float(params["reg_alpha"]),
                "max_bin": int(params["max_bin"]),
                "min_child_weight": int(params["min_child_weight"]),
            })
            
            rmses = []
            n_boost = int(params["n_estimators"])
            
            for tr_idx, va_idx in self.kf.split(X_train):
                X_tr, X_va = X_train.iloc[tr_idx], X_train.iloc[va_idx]
                y_tr, y_va = y_train.iloc[tr_idx], y_train.iloc[va_idx]
                
                dtr = xgb.DMatrix(X_tr, label=y_tr)
                dva = xgb.DMatrix(X_va, label=y_va)
                
                bst = xgb.train(
                    params=p,
                    dtrain=dtr,
                    num_boost_round=n_boost,
                    evals=[(dva, "valid")],
                    early_stopping_rounds=50,
                    verbose_eval=False
                )
                preds = bst.predict(dva, iteration_range=(0, bst.best_iteration + 1))
                rmses.append(rmse_from_arrays(y_va, preds))
            return float(np.mean(rmses))

        @use_named_args(self.ridge_space)
        def ridge_cv_objective(**params):
            alpha = float(params["alpha"])
            rmses = []
            for tr_idx, va_idx in self.kf.split(X_train):
                X_tr, X_va = X_train.iloc[tr_idx], X_train.iloc[va_idx]
                y_tr, y_va = y_train.iloc[tr_idx], y_train.iloc[va_idx]
                
                model = Ridge(alpha=alpha, random_state=self.seed)
                model.fit(X_tr, y_tr)
                preds = model.predict(X_va)
                rmses.append(rmse_from_arrays(y_va, preds))
            return float(np.mean(rmses))

        print("Executing Bayesian Optimization for Stage 1 Base Learners...")
        xgb_result = gp_minimize(func=xgb_cv_objective, dimensions=self.xgb_space, 
                                 n_calls=xgb_calls, n_initial_points=min(10, xgb_calls), 
                                 acq_func="EI", random_state=self.seed)
                                 
        ridge_result = gp_minimize(func=ridge_cv_objective, dimensions=self.ridge_space, 
                                   n_calls=ridge_calls, n_initial_points=min(8, ridge_calls), 
                                   acq_func="EI", random_state=self.seed)
        
        self.xgb_best = dict(zip([d.name for d in self.xgb_space], xgb_result.x))
        self.ridge_best_alpha = float(ridge_result.x[0])
        
        return self.xgb_best, self.ridge_best_alpha

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame) -> np.ndarray:
        """Generates out-of-fold meta-features and trains the second-stage meta-learner."""
        if not self.xgb_best:
            raise ValueError("Pipeline must optimize hyperparameters via .optimize_hyperparameters() before fitting.")

        oof_xgb = np.zeros(len(X_train))
        oof_ridge = np.zeros(len(X_train))
        test_preds_xgb = []
        test_preds_ridge = []
        
        print("\nConstructing Out-of-Fold Stacking Alignments...")
        for fold, (tr_idx, va_idx) in enumerate(self.kf.split(X_train), 1):
            X_tr, X_va = X_train.iloc[tr_idx], X_train.iloc[va_idx]
            y_tr, y_va = y_train.iloc[tr_idx], y_train.iloc[va_idx]
            
            # Reconstruct optimized XGBoost setup
            xgb_params = self.xgb_base_params.copy()
            xgb_params.update({
                "max_depth": int(self.xgb_best["max_depth"]),
                "learning_rate": float(self.xgb_best["learning_rate"]),
                "subsample": float(self.xgb_best["subsample"]),
                "colsample_bytree": float(self.xgb_best["colsample_bytree"]),
                "reg_lambda": float(self.xgb_best["reg_lambda"]),
                "reg_alpha": float(self.xgb_best["reg_alpha"]),
                "max_bin": int(self.xgb_best["max_bin"]),
                "min_child_weight": int(self.xgb_best["min_child_weight"]),
            })
            
            dtr = xgb.DMatrix(X_tr, label=y_tr)
            dva = xgb.DMatrix(X_va, label=y_va)
            dte = xgb.DMatrix(X_test)
            
            bst = xgb.train(
                params=xgb_params,
                dtrain=dtr,
                num_boost_round=int(self.xgb_best["n_estimators"]),
                evals=[(dva, "valid")],
                early_stopping_rounds=50,
                verbose_eval=False
            )
            
            oof_xgb[va_idx] = bst.predict(dva, iteration_range=(0, bst.best_iteration + 1))
            test_preds_xgb.append(bst.predict(dte, iteration_range=(0, bst.best_iteration + 1)))
            
            # Reconstruct optimized Ridge setup
            ridge_base = Ridge(alpha=self.ridge_best_alpha, random_state=self.seed)
            ridge_base.fit(X_tr, y_tr)
            oof_ridge[va_idx] = ridge_base.predict(X_va)
            test_preds_ridge.append(ridge_base.predict(X_test))

        # Format meta training and inference blocks
        X_meta_train = pd.DataFrame(
            np.column_stack([oof_xgb, oof_ridge]), 
            columns=['XGB_OOF', 'Ridge_OOF']
        )
        X_meta_test = pd.DataFrame(
            np.column_stack([
                np.mean(np.column_stack(test_preds_xgb), axis=1),
                np.mean(np.column_stack(test_preds_ridge), axis=1)
            ]), 
            columns=['XGB_OOF', 'Ridge_OOF']
        )
        
        # Train Meta-Learner Layer
        print("Training Second-Stage Meta-Ridge Learner...")
        self.meta_model = Ridge(alpha=0.1, random_state=self.seed)
        self.meta_model.fit(X_meta_train, y_train)
        
        return self.meta_model.predict(X_meta_test)

    def save_pipeline(self, filepath: str = "artifacts/HybridStack_model.pkl"):
        """Saves weights and optimal hyperparameters to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'meta_model': self.meta_model,
            'xgb_best': self.xgb_best,
            'ridge_best_alpha': self.ridge_best_alpha
        }, filepath)
        print(f"HybridStack components successfully exported to: {filepath}")


if __name__ == "__main__":
    # Structural functional evaluation with synthetic data inputs
    print("Generating validation synthetic context arrays...")
    np.random.seed(42)
    dummy_features = [f"Indicator_{i}" for i in range(8)]
    
    X_tr_raw = pd.DataFrame(np.random.randn(150, 8), columns=dummy_features)
    y_tr_raw = pd.Series(np.random.randn(150))
    X_te_raw = pd.DataFrame(np.random.randn(30, 8), columns=dummy_features)

    # Initialize execution pipeline
    pipeline = HybridStackPipeline(n_splits=3, seed=42)
    
    # Run rapid integration check
    pipeline.optimize_hyperparameters(X_tr_raw, y_tr_raw, xgb_calls=3, ridge_calls=2)
    test_predictions = pipeline.fit(X_tr_raw, y_tr_raw, X_te_raw)
    
    print("\nOptimal Parameter Selection Verification:")
    print(f" -> Best Ridge Alpha: {pipeline.ridge_best_alpha:.4f}")
    print(f" -> Predictions Shape Generated: {test_predictions.shape}")