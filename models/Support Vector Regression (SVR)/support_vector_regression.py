"""
Support Vector Regression (SVR) Pipeline.

This module provides a standalone, dataset-agnostic pipeline configuration 
for executing Grid Search Cross-Validation and optimizing a Support Vector 
Regression model with an RBF kernel.
"""

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR


def execute_svr_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for Support Vector Regression.

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
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base Support Vector Regression model with an RBF kernel
    svr_model = SVR(kernel="rbf")

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {
            "C": [1, 10, 100],
            "epsilon": [0.01, 0.1, 0.2],
            "gamma": ["scale", "auto"],
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=svr_model,
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
    X_tr = np.random.randn(150, 5)
    y_tr = np.random.randn(150)
    X_te = np.random.randn(20, 5)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_svr_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator()

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")