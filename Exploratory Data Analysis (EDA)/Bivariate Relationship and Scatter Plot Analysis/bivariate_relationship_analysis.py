"""
Bivariate Relationship and Scatter Plot Analysis Module
-------------------------------------------------------
A reusable, general-purpose framework for plotting professional bivariate 
scatter plots with regression overlays, enabling multi-feature exploration 
against a single reference target variable.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Union, Optional, Tuple


def plot_bivariate_relationships(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: Optional[Union[str, List[str]]] = None,
    n_cols: int = 3,
    figsize_per_plot: Tuple[int, int] = (6, 5),
    fit_reg: bool = True,
    alpha: float = 0.5,
    marker_color: str = "#2b5c8f",
    line_color: str = "#d95f02"
) -> Tuple[plt.Figure, pd.DataFrame]:
    """
    Generates a structured grid of scatter plots with regression lines, mapping multiple 
    continuous independent features against a single reference target variable. It also 
    computes localized Pearson and Spearman correlation parameters.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the features and target variable.
    target_col : str
        The primary continuous column used as the dependent variable (Y-axis).
    feature_cols : str or list of str, optional
        The independent continuous column(s) mapped on the X-axis. If None, 
        all numeric columns except the target will be selected automatically.
    n_cols : int, default=3
        The maximum number of column panels layout horizontally across the canvas.
    figsize_per_plot : tuple, default=(6, 5)
        Dimensions (width, height) assigned to each individual panel subplot.
    fit_reg : bool, default=True
        Whether to calculate and overlay an ordinary least squares regression trend line.
    alpha : float, default=0.5
        Opacity parameter applied to scatter markers to mitigate overplotting visibility issues.
    marker_color : str, default="#2b5c8f"
        Hex color code assigned to the data points.
    line_color : str, default="#d95f02"
        Hex color code assigned to the overlaid trend line.
        
    Returns:
    --------
    fig : matplotlib.figure.Figure
        The underlying figure canvas container.
    metrics_df : pd.DataFrame
        A quantitative tracking structure detailing Pearson and Spearman correlation factors.
    """
    # Validate target presence
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found within the input DataFrame.")
        
    # Isolate feature columns
    if feature_cols == None:
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_col in feature_cols:
            feature_cols.remove(target_col)
    elif isinstance(feature_cols, str):
        feature_cols = [feature_cols]
        
    # Eliminate any overlapping target column from feature listing
    feature_cols = [col for col in feature_cols if col in df.columns and col != target_col]
    
    if not feature_cols:
        raise ValueError("No valid numeric continuous columns were extracted for relationship plotting.")

    # Calculate correlation summaries
    correlation_metrics = []
    for col in feature_cols:
        # Isolate complete continuous matrix rows
        clean_subset = df[[col, target_col]].dropna()
        if len(clean_subset) > 1:
            pearson_val = clean_subset[col].corr(clean_subset[target_col], method="pearson")
            spearman_val = clean_subset[col].corr(clean_subset[target_col], method="spearman")
            correlation_metrics.append({
                "Independent Feature": col,
                "Pearson r": pearson_val,
                "Spearman rho": spearman_val
            })
    metrics_df = pd.DataFrame(correlation_metrics).set_index("Independent Feature")

    # Set up geometry parameters
    n_plots = len(feature_cols)
    n_rows = (n_plots + n_cols - 1) // n_cols
    total_figsize = (figsize_per_plot[0] * n_cols, figsize_per_plot[1] * n_rows)
    
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(n_rows, n_cols, figsize=total_figsize)
    
    # Flatten the matrix for reliable sequential parsing
    if n_plots == 1:
        axes = np.array([axes])
    else:
        axes = axes.flatten()

    # Build scatter canvases
    for idx, col in enumerate(feature_cols):
        ax = axes[idx]
        
        # Build scatter + regression line if requested
        sns.regplot(
            data=df,
            x=col,
            y=target_col,
            ax=ax,
            scatter_kws={"alpha": alpha, "color": marker_color, "edgecolor": "none"},
            line_kws={"color": line_color, "linewidth": 2.0} if fit_reg else {"visible": False},
            fit_reg=fit_reg
        )
        
        # Pull correlation values for label printing
        p_val = metrics_df.loc[col, "Pearson r"] if col in metrics_df.index else np.nan
        
        ax.set_title(f"{target_col} vs. {col}\n(r = {p_val:.2f})", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel(target_col, fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)

    # Erase visual windows for unassigned trailing axes
    for idx in range(n_plots, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    return fig, metrics_df


if __name__ == "__main__":
    # Example Demonstration using synthetic simulation parameters
    print("Generating simulated co-dependent variables for validation...")
    
    np.random.seed(42)
    n_observations = 500
    
    # Establish a simulated continuous baseline metric
    target = np.random.normal(loc=2.5, scale=0.5, size=n_observations)
    
    # Create variables with specific geometric mappings to the target
    linear_positive = target * 1.5 + np.random.normal(0, 0.2, n_observations)
    linear_negative = -2.0 * target + np.random.normal(0, 0.4, n_observations)
    non_linear_parabolic = (target - 2.5) ** 2 + np.random.normal(0, 0.05, n_observations)
    
    mock_df = pd.DataFrame({
        "Reference Target": target,
        "Linear Indicator A": linear_positive,
        "Linear Indicator B": linear_negative,
        "Curvilinear Feature": non_linear_parabolic
    })
    
    # Run the modular function
    fig, correlations = plot_bivariate_relationships(
        df=mock_df,
        target_col="Reference Target",
        feature_cols=["Linear Indicator A", "Linear Indicator B", "Curvilinear Feature"],
        n_cols=3,
        figsize_per_plot=(5, 4.5)
    )
    
    print("
--- Extracted Correlation Coefficients Matrix ---")
    print(correlations.round(4))
    
    # Save image file to verify functionality
    output_image = "bivariate_relationship_grid.png"
    fig.savefig(output_image, dpi=300)
    print(f"
Success! Reusable relationship module verified. Image asset saved: {output_image}")
