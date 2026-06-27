"""
Lasso Regression Pipeline with Grid Search Cross-Validation.

This module provides a standalone, production-ready pipeline configuration 
for feature standardization, hyperparameter tuning, and optimization of 
a Lasso Regression model.
"""

import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler


def execute_lasso_pipeline(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    max_iter: int = 5000,
    scoring: str = "neg_mean_squared_error",
    n_jobs: int = -1,
) -> tuple:
    """Standardizes input datasets, optimizes Lasso hyperparameter via GridSearchCV,

    and returns the best estimator along with predictions.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    X_test : np.ndarray
        Inference feature matrix.
    param_grid : dict, optional
        Dictionary mapping candidate alpha parameter lists.
    cv : int
        Number of cross-validation splitting folds.
    max_iter : int
        Maximum number of iterations allowed for the coordinate descent solver.
    scoring : str
        Evaluation metric used to score hyperparameter configurations.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    best_model : sklearn.linear_model.Lasso
        The optimized Lasso model retrained on the best parameter settings.
    best_params : dict
        The parameter map configuration that yielded the best validation score.
    predictions : np.ndarray
        Predicted values evaluated on the scaled test dataset.
    """
    # Initialize standardization scaler to ensure uniform regularization penalties
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize base Lasso Regressor with extended iteration limits for convergence stability
    lasso_model = Lasso(max_iter=max_iter)

    # Define default alpha grid search constraints if not customized
    if param_grid is None:
        param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}

    # Construct cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=lasso_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Perform structural optimization fit routines
    grid_search.fit(X_train_scaled, y_train)

    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    predictions = best_model.predict(X_test_scaled)

    return best_model, best_params, predictions


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic tests
    np.random.seed(42)

    print("Constructing synthetic dataset matrix blocks...")
    X_tr = np.random.randn(120, 6)
    y_tr = np.random.randn(120)
    X_te = np.random.randn(20, 6)

    print("Executing hyperparameter grid search optimization...")
    model, params, preds = execute_lasso_pipeline(X_train=X_tr, y_train=y_tr, X_test=X_te)

    print("\nOptimal Parameters Selected:")
    print(params)

    print(f"\nNon-zero coefficients: {np.sum(model.coef_ != 0)} out of {len(model.coef_)}")
    print(f"Inference complete. Predictions array shape: {preds.shape}")