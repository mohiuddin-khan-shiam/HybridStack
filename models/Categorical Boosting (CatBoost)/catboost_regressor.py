"""
CatBoost Regressor Pipeline with Grid Search Cross-Validation.

This module provides a standalone, production-ready implementation for 
initializing, tuning, and optimizing a CatBoost Regressor independently of 
any project-specific dataset details.
"""

import warnings
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import GridSearchCV

# Suppress internal runtime casting warnings raised by Scikit-Learn structures
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="invalid value encountered in cast",
)


def execute_catboost_grid_search(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    X_val: pd.DataFrame = None,
    y_val: np.ndarray = None,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    random_state: int = 42,
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for a CatBoost Regressor.

    Parameters:
    -----------
    X_train : pd.DataFrame or np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous labels.
    X_val : pd.DataFrame or np.ndarray, optional
        Validation feature matrix used specifically to enforce early stopping.
    y_val : np.ndarray, optional
        Validation target values paired with X_val.
    param_grid : dict, optional
        Dictionary mapping hyperparameter configurations to optimize over.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to rank hyperparameter configurations.
    random_state : int
        Seed value for the internal random number generator for reproducibility.
    n_jobs : int
        Number of parallel worker jobs. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base CatBoost Regressor with essential tracking settings
    cat_model = CatBoostRegressor(random_state=random_state, verbose=0)

    # Establish default multi-dimensional search space domain if not specified
    if param_grid is None:
        param_grid = {
            "iterations": [300, 500, 1000],
            "learning_rate": [0.01, 0.05, 0.1],
            "depth": [4, 6, 8],
            "early_stopping_rounds": [50, 100],
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=cat_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Define fit parameters for the underlying base model
    fit_params = {"verbose": False}
    if X_val is not None and y_val is not None:
        fit_params["eval_set"] = (X_val, y_val)

    # Execute hyperparameter search optimization
    grid_search.fit(X_train, y_train, **fit_params)

    return grid_search


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic testing
    np.random.seed(42)

    print("Constructing synthetic dataset blocks...")
    X_tr = pd.DataFrame(np.random.randn(200, 6), columns=[f"Num_{i}" for i in range(6)])
    y_tr = np.random.randn(200)
    
    X_va = pd.DataFrame(np.random.randn(50, 6), columns=[f"Num_{i}" for i in range(6)])
    y_va = np.random.randn(50)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_catboost_grid_search(
        X_train=X_tr, y_train=y_tr, X_val=X_va, y_val=y_va
    )

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_va)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")