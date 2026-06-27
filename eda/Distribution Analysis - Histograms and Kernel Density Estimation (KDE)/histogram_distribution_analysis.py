"""
Module Name: histogram_distribution_analysis.py
Description: A reusable, modular script to analyze continuous numerical data distributions 
             using histograms and Kernel Density Estimation (KDE) overlays inside 
             dynamic grid subplots.
"""

import os
import math
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_univariate_distributions(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    bins: int = 30,
    kde: bool = True,
    max_cols_per_row: int = 2,
    figsize_per_plot: Tuple[int, int] = (7, 5),
    title: str = "Univariate Distribution Analysis",
    xlabel_suffix: str = "",
    save_path: Optional[str] = None,
) -> None:
    """Generates a structured grid of histograms with KDE overlays for continuous variables.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the numerical features.
    columns : Optional[List[str]], default None
        List of target numerical columns to plot. If None, automatically selects all numerical features.
    bins : int, default 30
        The number of bins or intervals to slice the continuous data space into.
    kde : bool, default True
        If True, overlays a continuous Kernel Density Estimation line over the histogram.
    max_cols_per_row : int, default 2
        The maximum number of subplots to display side-by-side per row on the canvas grid.
    figsize_per_plot : Tuple[int, int], default (7, 5)
        The dimension blueprint (width, height) allocated for each individual subplot frame.
    title : str, default 'Univariate Distribution Analysis'
        The overarching title text placed at the top of the combined figure grid.
    xlabel_suffix : str, default ''
        An optional suffix string appended to the x-axis label of every subplot (e.g., ' (%)' or ' (USD)').
    save_path : Optional[str], default None
        The explicit system file path used to write out the final high-resolution chart image.
    """
    # Auto-extract numerical columns if none specified
    target_columns = columns if columns else df.select_dtypes(include=["number"]).columns.tolist()

    if not target_columns:
        raise ValueError("No valid numerical features were discovered or provided for analysis.")

    num_plots = len(target_columns)
    
    # Calculate grid structural dynamics
    cols = min(num_plots, max_cols_per_row)
    rows = math.ceil(num_plots / cols)

    # Calculate overall figure dimensions dynamically
    fig_width = cols * figsize_per_plot[0]
    fig_height = rows * figsize_per_plot[1]

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height), squeeze=False)
    
    # Flatten axes array for straightforward loop iteration tracking
    axes_flat = axes.flatten()

    for idx, col in enumerate(target_columns):
        ax = axes_flat[idx]
        
        if col not in df.columns:
            print(f"[Warning] Target column '{col}' not found in DataFrame. Skipping.")
            ax.axis("off")
            continue

        # Drop missing values to prevent visualization errors
        clean_series = df[col].dropna()

        if clean_series.empty:
            print(f"[Warning] Column '{col}' contains only null values. Skipping.")
            ax.axis("off")
            continue

        # Plot the histogram combined with the continuous KDE curve
        sns.histplot(
            data=clean_series,
            bins=bins,
            kde=kde,
            ax=ax,
            color="steelblue",
            edgecolor="white",
            alpha=0.7
        )

        # Style individual plot components
        ax.set_title(f"Distribution of {col}", fontsize=12, fontweight="semibold", pad=10)
        ax.set_xlabel(f"{col}{xlabel_suffix}", fontsize=10, labelpad=8)
        ax.set_ylabel("Frequency Count", fontsize=10, labelpad=8)

    # Hide any unused subplots in the grid layout
    for idx in range(num_plots, len(axes_flat)):
        axes_flat[idx].axis("off")

    # Attach the primary global layout configurations
    plt.suptitle(title, fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    # Save the output visualization asset if requested
    if save_path:
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Info] Distribution chart grid successfully saved to: {save_path}")

    plt.show()
    plt.close()


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    import numpy as np

    # Generating a structured synthetic dataset to test diverse distribution profiles
    np.random.seed(42)
    samples = 500

    dummy_data = pd.DataFrame(
        {
            "Normal_Economic_Indicator": np.random.normal(loc=2.0, scale=0.5, size=samples),
            "Skewed_Market_Indicator": np.random.exponential(scale=1.5, size=samples),
            "Bimodal_Sentiment_Indicator": np.concatenate(
                [
                    np.random.normal(loc=1.0, scale=0.3, size=samples // 2),
                    np.random.normal(loc=4.5, scale=0.4, size=samples // 2),
                ]
            ),
        }
    )

    print("--- 1. Executing Grid Distribution Analysis ---")
    print("[Note] This will process all columns and organize them into an iterable grid layout.")
    plot_univariate_distributions(
        df=dummy_data,
        columns=[
            "Normal_Economic_Indicator",
            "Skewed_Market_Indicator",
            "Bimodal_Sentiment_Indicator",
        ],
        bins=25,
        max_cols_per_row=2,
        title="Comprehensive Macro Indicator Distribution Profile",
        xlabel_suffix=" (%)",
    )