"""
Ridge Regression Pipeline with Grid Search Cross-Validation.

This module provides a standalone, dataset-agnostic pipeline configuration 
for initializing, tuning, and optimizing a Ridge Regression model using 
an analytical closed-form configuration.
"""

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV


def execute_ridge_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for a Ridge Regression estimator.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary mapping hyperparameter names to candidate array lists.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to rank hyperparameter configurations.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize base Ridge regression model
    ridge_model = Ridge()

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {"alpha": [0.1, 1.0, 10.0, 100.0, 1000.0]}

    # Construct cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=ridge_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Perform structural optimization fit routines
    grid_search.fit(X_train, y_train)

    return grid_search


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic tests
    np.random.seed(42)

    print("Constructing synthetic dataset matrix blocks...")
    X_tr = np.random.randn(100, 4)
    y_tr = np.random.randn(100)
    X_te = np.random.randn(15, 4)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_ridge_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")