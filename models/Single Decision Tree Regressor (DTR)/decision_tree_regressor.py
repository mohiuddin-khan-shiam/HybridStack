"""
Decision Tree Regressor Pipeline with Grid Search Cross-Validation.

This module provides a standalone, production-ready pipeline configuration 
for initializing, tuning, and optimizing a Decision Tree Regressor 
independent of specific project details.
"""

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor


def execute_decision_tree_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    random_state: int = 42,
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for a Decision Tree Regressor.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary specifying hyperparameter search options.
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
    # Initialize the base Decision Tree Regressor
    dt_model = DecisionTreeRegressor(random_state=random_state)

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {
            "max_depth": [3, 5, 7, 10, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["sqrt", "log2", None],
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=dt_model,
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
    X_tr = np.random.randn(200, 6)
    y_tr = np.random.randn(200)
    X_te = np.random.randn(30, 6)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_decision_tree_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")