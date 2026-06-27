"""
Module Name: pairwise_relationship_analysis.py
Description: A reusable, modular script to execute pairwise relationship analyses 
             using pair plots (scatter plot matrices) with customizable distributions, 
             marker styling, and clear axis management.
"""

import os
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_pairwise_relationships(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    rename_mapping: Optional[Dict[str, str]] = None,
    hue_column: Optional[str] = None,
    diag_kind: str = "kde",
    marker_size: float = 6.0,
    marker_alpha: float = 0.5,
    plot_height: float = 3.0,
    title: str = "Pairwise Relationship Analysis Matrix",
    save_path: Optional[str] = None,
) -> None:
    """Generates a highly readable, stylized pair plot matrix for multivariate numerical analysis.

    Parameters:
    -----------
    df : pd.DataFrame
        The target source input DataFrame.
    columns : Optional[List[str]], default None
        List of continuous numerical features to plot. If None, selects all numerical columns.
    rename_mapping : Optional[Dict[str, str]], default None
        A mapping dictionary to shorten long column names for better grid readability.
    hue_column : Optional[str], default None
        An optional categorical feature name used to color-code scatter markers.
    diag_kind : str, default 'kde'
        Type of visualization for the main diagonal cells: {'kde', 'hist', None}.
    marker_size : float, default 6.0
        The structural scale/size ('s') configuration for the individual scatter points.
    marker_alpha : float, default 0.5
        Transparency setting for scatter points to mitigate overplotting challenges.
    plot_height : float, default 3.0
        The spatial canvas height dimension for each individual square subplot inside the grid.
    title : str, default 'Pairwise Relationship Analysis Matrix'
        The comprehensive title string added above the plot matrix layout.
    save_path : Optional[str], default None
        System file path to export the completed high-resolution visualization asset.
    """
    # Isolate targets and create a shallow copy to prevent editing original structures
    target_cols = columns.copy() if columns else df.select_dtypes(include=["number"]).columns.tolist()

    if hue_column and hue_column in df.columns:
        # Ensure hue column is tracked without causing duplicate entry errors
        if hue_column in target_cols:
            target_cols.remove(hue_column)
        working_df = df[target_cols + [hue_column]].copy()
    else:
        working_df = df[target_cols].copy()

    # Apply column renames to optimize grid legibility if provided
    if rename_mapping:
        working_df.rename(columns=rename_mapping, inplace=True)
        # Re-map target names list to handle layout loop steps correctly
        target_cols = [rename_mapping.get(c, c) for c in target_cols]

    # Drop incomplete data rows to ensure unbroken grid generation
    working_df.dropna(inplace=True)

    if working_df.empty:
        raise ValueError("DataFrame is empty after dropping missing row indices.")

    sns.set_theme(style="whitegrid")

    # Generate the base pair plot grid structure
    pair_grid = sns.pairplot(
        data=working_df,
        vars=target_cols,
        hue=hue_column,
        diag_kind=diag_kind,
        height=plot_height,
        palette="Dark2" if hue_column else None,
        plot_kws={"s": marker_size, "alpha": marker_alpha}
    )

    # Format subplot axes for clear, non-overlapping label visibility
    for ax in pair_grid.axes.flatten():
        if ax is not None:
            ax.set_xlabel(ax.get_xlabel(), fontsize=10, labelpad=8)
            ax.set_ylabel(ax.get_ylabel(), fontsize=10, labelpad=8)
            ax.tick_params(axis="x", labelrotation=30, labelsize=9)
            ax.tick_params(axis="y", labelsize=9)

    # Attach the primary overarching title context
    plt.suptitle(title, fontsize=14, fontweight="bold", y=1.02)

    if save_path:
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Info] Pairwise plot matrix successfully saved to: {save_path}")

    plt.show()
    plt.close()


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    import numpy as np

    # Generating a structured synthetic dataset representing diverse economic profiles
    np.random.seed(42)
    samples = 150

    dummy_df = pd.DataFrame(
        {
            "Macro_Indicator_Inflation_Rate_Long": np.random.normal(3.0, 1.0, samples),
            "Macro_Indicator_Gross_Product_Long": np.random.normal(2.5, 0.5, samples),
            "Macro_Indicator_Employment_Rate_Long": np.random.normal(5.0, 1.2, samples),
            "Economic_Regime_Class": np.random.choice(["Regime_Alpha", "Regime_Beta"], samples),
        }
    )

    # Introduce a deterministic linear interaction path to verify pattern isolation
    dummy_df["Macro_Indicator_Employment_Rate_Long"] += (
        dummy_df["Macro_Indicator_Inflation_Rate_Long"] * 0.8
    )

    # Configure a clean rename dictionary to minimize axis footprint space
    aliases = {
        "Macro_Indicator_Inflation_Rate_Long": "INF",
        "Macro_Indicator_Gross_Product_Long": "GDP",
        "Macro_Indicator_Employment_Rate_Long": "EMP",
    }

    print("--- 1. Rendering Unsupervised Pairwise Plot ---")
    plot_pairwise_relationships(
        df=dummy_df,
        columns=[
            "Macro_Indicator_Inflation_Rate_Long",
            "Macro_Indicator_Gross_Product_Long",
            "Macro_Indicator_Employment_Rate_Long",
        ],
        rename_mapping=aliases,
        title="Economic Indicators Structural Matrix (Unsupervised)",
    )

    print("\n--- 2. Rendering Class-Stratified Pairwise Plot ---")
    plot_pairwise_relationships(
        df=dummy_df,
        columns=[
            "Macro_Indicator_Inflation_Rate_Long",
            "Macro_Indicator_Gross_Product_Long",
            "Macro_Indicator_Employment_Rate_Long",
        ],
        rename_mapping=aliases,
        hue_column="Economic_Regime_Class",
        title="Economic Indicators Matrix Split by Regime Class",
    )