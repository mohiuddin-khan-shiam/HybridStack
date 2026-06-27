"""
Extreme Gradient Boosting (XGBoost) Regressor Pipeline.

This module provides a robust, standalone pipeline configuration for executing 
Grid Search Cross-Validation and final model optimization using XGBoost.
"""

from itertools import product
import numpy as np
import xgboost as xgb


def execute_xgboost_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    param_grid: dict = None,
    base_params: dict = None,
    n_folds: int = 5,
    num_boost_round: int = 200,
    early_stopping_rounds: int = 10,
    seed: int = 42,
) -> tuple:
    """Performs a manual Grid Search with Cross-Validation over the specified parameter

    grid and trains an optimized XGBoost Regressor model.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target vector.
    X_test : np.ndarray
        Testing/Validation feature matrix.
    y_test : np.ndarray
        Testing/Validation target vector.
    param_grid : dict, optional
        Dictionary mapping hyperparameter names to lists of options.
    base_params : dict, optional
        Dictionary of baseline parameters constant across all iterations.
    n_folds : int
        Number of cross-validation folds.
    num_boost_round : int
        Maximum number of boosting trees to build.
    early_stopping_rounds : int
        Validation improvement patience threshold.
    seed : int
        Random state seed value for reproducibility.

    Returns:
    --------
    best_xgb_model : xgb.Booster
        The final trained booster model optimized with the best parameters.
    best_params : dict
        The parameter configuration that yielded the minimum cross-validation error.
    predictions : np.ndarray
        Model inference values evaluated on the test dataset matrix.
    """
    # Set default grid values if not provided
    if param_grid is None:
        param_grid = {
            "max_depth": [3, 6, 9],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.7, 0.8, 0.9],
            "colsample_bytree": [0.7, 0.8, 0.9],
        }

    if base_params is None:
        base_params = {
            "objective": "reg:squarederror",
            "eval_metric": "rmse",
            "seed": seed,
        }

    # Convert datasets to specialized optimized DMatrix containers
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    best_params = None
    best_rmse = float("inf")

    # Generate the cartesian product of all hyperparameter combinations
    keys, values = zip(*param_grid.items())
    experiments = [dict(zip(keys, v)) for v in product(*values)]

    print(f"Starting Grid Search across {len(experiments)} configurations...")

    for i, config in enumerate(experiments, start=1):
        params = base_params.copy()
        params.update(config)

        # Run internal XGBoost cross-validation routines
        cv_results = xgb.cv(
            params=params,
            dtrain=dtrain,
            num_boost_round=num_boost_round,
            nfold=n_folds,
            early_stopping_rounds=early_stopping_rounds,
            metrics="rmse",
            seed=seed,
            verbose_eval=False,
        )

        mean_rmse = cv_results["test-rmse-mean"].min()

        if mean_rmse < best_rmse:
            best_rmse = mean_rmse
            best_params = params

    print(f"Grid Search Complete. Best CV RMSE: {best_rmse:.5f}")

    # Retrain final optimal framework model
    best_xgb_model = xgb.train(
        params=best_params,
        dtrain=dtrain,
        num_boost_round=num_boost_round,
        evals=[(dtest, "test")],
        early_stopping_rounds=early_stopping_rounds,
        verbose_eval=False,
    )

    predictions = best_xgb_model.predict(dtest)

    return best_xgb_model, best_params, predictions


if __name__ == "__main__":
    # Generate synthetic regression dataset variables for standalone testing
    np.random.seed(42)
    X_tr = np.random.randn(150, 8)
    y_tr = np.random.randn(150)
    X_te = np.random.randn(30, 8)
    y_te = np.random.randn(30)

    # Execute structural optimization pipeline
    model, hyperparameters, preds = execute_xgboost_grid_search(
        X_train=X_tr, y_train=y_tr, X_test=X_te, y_test=y_te
    )

    print("
Optimized Parameters Selected:")
    for k, v in hyperparameters.items():
        print(f"  {k}: {v}")

    print(f"
Predictions successfully generated. Count: {len(preds)}")
