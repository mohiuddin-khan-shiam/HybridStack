"""
Histogram-Based Gradient Boosting Regressor Pipeline.

This module provides a standalone, production-ready configuration for 
executing Grid Search Cross-Validation and final model optimization using 
Scikit-Learn's HistGradientBoostingRegressor framework.
"""

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GridSearchCV


def execute_hgb_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    random_state: int = 42,
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for a Histogram-Based Gradient

    Boosting Regressor.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary specifying the hyperparameter search space configurations.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to rank hyperparameter configurations.
    random_state : int
        Seed value for the internal random number generator for reproducibility.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base histogram-based estimator
    hgb_model = HistGradientBoostingRegressor(random_state=random_state)

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {
            "max_iter": [100, 200, 300],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 5, 7],
            "min_samples_leaf": [10, 20, 50],
            "max_bins": [255, 128, 100],
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=hgb_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Perform optimization fit routines
    grid_search.fit(X_train, y_train)

    return grid_search


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic tests
    np.random.seed(42)

    print("Constructing synthetic dataset matrix blocks...")
    X_tr = np.random.randn(500, 10)
    y_tr = np.random.randn(500)
    X_te = np.random.randn(50, 10)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_hgb_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")