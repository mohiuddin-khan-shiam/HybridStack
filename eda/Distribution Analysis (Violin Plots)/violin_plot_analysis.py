"""
Module Name: violin_plot_analysis.py
Description: A reusable, modular script to perform distribution analysis using
             violin plots. Supports single/multi-feature evaluation, categorical 
             stratification, and split-half configurations.
"""

import os
from typing import List, Optional
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_distribution_violins(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    group_by: Optional[str] = None,
    split_half: bool = False,
    orient: str = "v",
    inner: str = "box",
    bw_adjust: float = 1.0,
    title: str = "Distribution Violin Plot",
    ylabel: str = "Values",
    xlabel: str = "Features",
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None,
) -> None:
    """Generates and displays a styled violin plot to visualize continuous data distributions.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the numerical data.
    columns : Optional[List[str]], default None
        List of target numerical column names to map. If None, uses all numerical columns.
    group_by : Optional[str], default None
        Categorical column name used to partition data into parallel sub-violins.
    split_half : bool, default False
        If True and group_by has exactly two levels, splits each violin in half to compare groups.
    orient : str, default 'v'
        Orientation of the plot: 'v' for vertical, 'h' for horizontal.
    inner : str, default 'box'
        Representation of the data's interior: {'box', 'quartiles', 'point', 'stick', None}.
    bw_adjust : float, default 1.0
        Bandwidth adjustment factor. Lower values make the curve more detailed; higher values smoother.
    title : str, default 'Distribution Violin Plot'
        Plot title text.
    ylabel : str, default 'Values'
        Y-axis label string.
    xlabel : str, default 'Features'
        X-axis label string.
    figsize : tuple, default (10, 6)
        Visual dimensions of the output canvas.
    save_path : Optional[str], default None
        System path target to save the generated image asset.
    """
    plt.figure(figsize=figsize)
    sns.set_theme(style="whitegrid")

    # Isolate numerical columns if none specified
    target_columns = columns if columns else df.select_dtypes(include=["number"]).columns.tolist()

    if group_by:
        if not columns or len(columns) != 1:
            raise ValueError(
                "When using 'group_by', you must specify exactly one numerical column via 'columns'."
            )
        
        # Plotting a single numeric feature stratified by a categorical column
        sns.violinplot(
            data=df,
            x=group_by if orient == "v" else target_columns[0],
            y=target_columns[0] if orient == "v" else group_by,
            hue=group_by if split_half else None,
            split=split_half,
            orient=orient,
            inner=inner,
            bw_adjust=bw_adjust,
            palette="muted"
        )
        if xlabel == "Features":
            xlabel = group_by
        if ylabel == "Values":
            ylabel = target_columns[0]
    else:
        # Plotting multiple numeric columns side-by-side
        sns.violinplot(
            data=df[target_columns],
            orient=orient,
            inner=inner,
            bw_adjust=bw_adjust,
            palette="Set2"
        )

    plt.title(title, fontsize=14, pad=15)
    
    if orient == "v":
        plt.xlabel(xlabel, fontsize=11, labelpad=10)
        plt.ylabel(ylabel, fontsize=11, labelpad=10)
        plt.xticks(rotation=15, ha="right")
    else:
        plt.xlabel(ylabel, fontsize=11, labelpad=10)
        plt.ylabel(xlabel, fontsize=11, labelpad=10)

    plt.tight_layout()

    if save_path:
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path, dpi=300)
        print(f"[Info] Violin plot successfully saved to: {save_path}")

    plt.show()
    plt.close()


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    import numpy as np

    # Generating a dummy synthetic dataset with explicit distribution characteristics
    np.random.seed(42)
    sample_size = 300

    # Create a clean unimodal distribution
    unimodal_data = np.random.normal(loc=2.5, scale=0.7, size=sample_size)

    # Create a distinct bimodal distribution (two clear peaks)
    bimodal_part1 = np.random.normal(loc=1.0, scale=0.4, size=sample_size // 2)
    bimodal_part2 = np.random.normal(loc=5.0, scale=0.5, size=sample_size // 2)
    bimodal_data = np.concatenate([bimodal_part1, bimodal_part2])

    dummy_df = pd.DataFrame(
        {
            "Unimodal_Feature": unimodal_data,
            "Bimodal_Feature": bimodal_data,
            "Category_Group": np.random.choice(["Group_A", "Group_B"], size=sample_size),
        }
    )

    print("--- 1. Rendering Multi-Feature Violin Plot ---")
    print("[Note] Look for the dual-bulges on Bimodal_Feature compared to Unimodal_Feature.")
    plot_distribution_violins(
        df=dummy_df,
        columns=["Unimodal_Feature", "Bimodal_Feature"],
        title="Comparative Distribution Analysis (Unimodal vs Bimodal)",
        ylabel="Scale Value",
    )

    print("\n--- 2. Rendering Stratified Split Violin Plot ---")
    plot_distribution_violins(
        df=dummy_df,
        columns=["Bimodal_Feature"],
        group_by="Category_Group",
        split_half=True,
        title="Split Categorical Comparison of Bimodal Distributions",
        ylabel="Scale Value",
        xlabel="Subgroups"
    )