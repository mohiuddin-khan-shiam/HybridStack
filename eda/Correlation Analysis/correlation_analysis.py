"""
Module Name: correlation_analysis.py
Description: A reusable, modular script to perform global correlation analysis 
             on numerical features within a dataset, producing matrix summaries 
             and stylized heatmap visualizations.
"""

import os
from typing import List, Optional
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def compute_correlation_matrix(
    df: pd.DataFrame, method: str = "pearson"
) -> pd.DataFrame:
    """Computes the pairwise correlation matrix for numerical columns in a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        The input dataframe containing numerical features.
    method : str, default 'pearson'
        Correlation method to use: {'pearson', 'spearman', 'kendall'}.

    Returns:
    --------
    pd.DataFrame
        A symmetric matrix containing correlation coefficients.
    """
    # Isolate only numerical columns
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise ValueError(
            "The provided DataFrame does not contain any numerical columns."
        )

    return numeric_df.corr(method=method)


def plot_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    title: str = "Correlation Heatmap",
    cmap: str = "coolwarm",
    figsize: tuple = (12, 8),
    save_path: Optional[str] = None,
) -> None:
    """Generates and displays a clean, well-formatted correlation heatmap.

    Parameters:
    -----------
    corr_matrix : pd.DataFrame
        The symmetric correlation matrix to visualize.
    title : str, default 'Correlation Heatmap'
        The title string for the generated plot.
    cmap : str, default 'coolwarm'
        The color map configuration for Seaborn.
    figsize : tuple, default (12, 8)
        The structural dimensions (width, height) of the figure.
    save_path : Optional[str], default None
        File path to save the generated figure. If None, the image is not saved.
    """
    plt.figure(figsize=figsize)

    # Generate a clean heatmap with annotations
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap=cmap,
        fmt=".2f",
        linewidths=0.5,
        vmin=-1.0,
        vmax=1.0,  # Explicitly bind scale boundaries
        cbar_kws={"label": "Correlation Coefficient"},
    )

    plt.title(title, fontsize=14, pad=15)
    plt.tight_layout()

    if save_path:
        # Create directory if it doesn't exist
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path, dpi=300)
        print(f"[Info] Plot successfully saved to: {save_path}")

    plt.show()
    plt.close()


def find_highly_correlated_pairs(
    corr_matrix: pd.DataFrame, threshold: float = 0.8
) -> pd.DataFrame:
    """Identifies and extracts feature pairs with a correlation coefficient

    above a specified absolute threshold (excluding diagonal matches).

    Parameters:
    -----------
    corr_matrix : pd.DataFrame
        The symmetric correlation matrix.
    threshold : float, default 0.8
        The absolute threshold value to screen for (0.0 to 1.0).

    Returns:
    --------
    pd.DataFrame
        A long-form DataFrame tracking Feature 1, Feature 2, and their Correlation.
    """
    pairs = []
    columns = corr_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                pairs.append(
                    {"Feature 1": columns[i], "Feature 2": columns[j], "Correlation": val}
                )

    return pd.DataFrame(pairs).sort_values(by="Correlation", ascending=False)


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    # Generating dummy numerical dataset for standalone testing execution
    import numpy as np

    np.random.seed(42)
    dummy_data = pd.DataFrame(
        {
            "Indicator_A": np.random.rand(100) * 100,
            "Indicator_B": np.random.rand(100) * 50,
            "Non_Linear": np.linspace(1, 100, 100) ** 2,
        }
    )
    # Inject an intentional strong correlation
    dummy_data["Indicator_C"] = dummy_data["Indicator_A"] * 2.5 + np.random.normal(
        0, 10, 100
    )

    print("--- 1. Computing Matrix ---")
    matrix = compute_correlation_matrix(dummy_data, method="pearson")
    print(matrix)

    print("\n--- 2. Finding High Correlations (|r| >= 0.7) ---")
    high_corr = find_highly_correlated_pairs(matrix, threshold=0.7)
    print(high_corr)

    print("\n--- 3. Rendering Visualization ---")
    plot_correlation_heatmap(
        matrix, title="Demo Correlation Analysis", save_path=None
    )