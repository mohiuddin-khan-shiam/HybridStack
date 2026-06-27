"""
Partial Dependence Plots (PDP) Visualization Pipeline.

This module provides a standalone, dataset-agnostic framework for calculating
and rendering publication-quality individual and bivariate Partial Dependence Plots
using Scikit-Learn's inspection utilities.
"""

import os
from typing import List, Union, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import PartialDependenceDisplay


def generate_partial_dependence_plots(
    estimator: getattr,
    X_eval: pd.DataFrame,
    features_to_plot: List[Union[int, str]],
    kind: str = "average",
    grid_resolution: int = 50,
    subsample: Optional[Union[int, float]] = None,
    n_cols: int = 4,
    figsize: Tuple[float, float] = (18, 12),
    title: Optional[str] = None,
    output_path: Optional[str] = None,
    dpi: int = 300
) -> PartialDependenceDisplay:
    """Calculates partial dependence values and renders a grid layout display.

    Parameters:
    -----------
    estimator : fitted sklearn estimator
        A trained machine learning model that implements `predict` or `predict_proba`.
    X_eval : pd.DataFrame
        The dataset matrix used to compute the marginal baseline averages.
    features_to_plot : List[Union[int, str]]
        The list of feature names or column indices to evaluate on the grid.
    kind : str
        The type of line to generate: 'average' (PDP), 'individual' (ICE), 
        or 'both'.
    grid_resolution : int
        The number of evenly spaced points evaluated along each feature range.
    subsample : int or float, optional
        Fraction or absolute count of rows used to limit prediction costs.
    n_cols : int
        The number of subplots to arrange horizontally in the grid layout.
    figsize : Tuple[float, float]
        Dimensions of the output figure in inches (width, height).
    title : str, optional
        Main title string to superimpose above the subplot grid.
    output_path : str, optional
        The destination file path to export the finished graphic to disk.
    dpi : int
        The dots-per-inch resolution quality constraint.

    Returns:
    --------
    display : PartialDependenceDisplay
        The fitted display object containing the figure and axis handles.
    """
    print(f"Calculating partial dependence profiles for features: {features_to_plot}...")
    
    # Generate the subplots and compute partial dependence
    display = PartialDependenceDisplay.from_estimator(
        estimator=estimator,
        X=X_eval,
        features=features_to_plot,
        kind=kind,
        grid_resolution=grid_resolution,
        subsample=subsample,
        n_cols=n_cols,
        random_state=42,
        n_jobs=-1
    )
    
    # Adjust layout settings and figure dimensions
    display.figure_.set_size_inches(figsize[0], figsize[1])
    
    if title:
        display.figure_.suptitle(title, fontsize=16, y=1.02)
        
    display.figure_.subplots_adjust(wspace=0.3, hspace=0.4)
    plt.tight_layout()
    
    # Export to disk if a destination path is provided
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        display.figure_.savefig(output_path, dpi=dpi, bbox_inches="tight")
        print(f"Successfully exported plot container to: {output_path}")
        
    return display


if __name__ == "__main__":
    # Standalone pipeline verification using synthetic models and arrays
    from sklearn.ensemble import RandomForestRegressor
    
    print("Setting up synthetic regression validation environment...")
    np.random.seed(42)
    feature_names = [f"Variable_{i}" for i in range(6)]
    
    # Generate mock training data
    X_mock = pd.DataFrame(np.random.randn(200, 6), columns=feature_names)
    # Target variable incorporates non-linear and interaction transformations
    y_mock = (
        X_mock["Variable_0"] * 2.5 
        + np.sin(X_mock["Variable_1"] * 1.5) 
        + np.exp(X_mock["Variable_2"] * 0.5)
    )
    
    # Fit a baseline black-box regressor model
    mock_model = RandomForestRegressor(n_estimators=20, random_state=42)
    mock_model.fit(X_mock, y_mock)
    
    # Define features to inspect
    target_features = ["Variable_0", "Variable_1", "Variable_2", ("Variable_0", "Variable_1")]
    
    # Run pipeline verification and export results
    os.makedirs("artifacts_test", exist_ok=True)
    pdp_display = generate_partial_dependence_plots(
        estimator=mock_model,
        X_eval=X_mock,
        features_to_plot=target_features,
        kind="average",
        n_cols=2,
        figsize=(12, 10),
        title="Partial Dependence Verification Suite",
        output_path="artifacts_test/pdp_diagnostic_sample.png"
    )
    
    print("\nPipeline execution completed successfully.")
    plt.close(pdp_display.figure_)