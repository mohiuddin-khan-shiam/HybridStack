"""
Module Name: categorical_aggregation_analysis.py
Description: A reusable, modular script to perform categorical aggregation analysis, 
             computing group summary statistics and rendering stylized bar charts.
"""

import os
from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def compute_group_aggregations(
    df: pd.DataFrame,
    group_by_col: str,
    target_col: str,
    agg_func: str = "mean"
) -> pd.Series:
    """Groups a DataFrame by a specified column and calculates an aggregate statistic

    for a target numerical feature.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the data.
    group_by_col : str
        The name of the categorical or discrete column used to group rows.
    target_col : str
        The continuous numerical column to be aggregated.
    agg_func : str, default 'mean'
        The aggregation operation to perform: {'mean', 'median', 'sum', 'count', 'std'}.

    Returns:
    --------
    pd.Series
        A Pandas Series indexed by the unique category groups, containing the aggregated results.
    """
    if group_by_col not in df.columns:
        raise KeyError(f"Grouping column '{group_by_col}' was not discovered in the DataFrame.")
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' was not discovered in the DataFrame.")

    # Drop records containing missing values in either column to ensure clean aggregation
    clean_df = df[[group_by_col, target_col]].dropna()

    if clean_df.empty:
        raise ValueError("DataFrame is empty after removing rows with missing values.")

    aggregated_series = clean_df.groupby(group_by_col)[target_col].agg(agg_func)
    return aggregated_series


def plot_aggregation_bars(
    aggregated_data: pd.Series,
    orient: str = "v",
    sort_values: bool = False,
    ascending: bool = False,
    color_palette: str = "Blues_r",
    title: str = "Categorical Aggregation Summary",
    xlabel: str = "Categories",
    ylabel: str = "Aggregated Value",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None,
) -> None:
    """Generates and displays a clean, professionally formatted bar chart 

    based on pre-aggregated series information.

    Parameters:
    -----------
    aggregated_data : pd.Series
        An aggregated Pandas Series where indices represent labels and values hold metrics.
    orient : str, default 'v'
        Orientation of the chart layout: 'v' for vertical bars, 'h' for horizontal bars.
    sort_values : bool, default False
        If True, sorts categories by their aggregated metric values rather than keeping their index sequence.
    ascending : bool, default False
        Sorting direction if sort_values is configured to True.
    color_palette : str, default 'Blues_r'
        Color palette template to apply to the bars.
    title : str, default 'Categorical Aggregation Summary'
        The main descriptive title string for the plot window.
    xlabel : str, default 'Categories'
        Label string for the horizontal categorical axis.
    ylabel : str, default 'Aggregated Value'
        Label string for the vertical numerical axis.
    figsize : Tuple[int, int], default (12, 6)
        The explicit width and height dimensions of the output canvas.
    save_path : Optional[str], default None
        The target system file path to save the generated high-resolution visualization asset.
    """
    plot_series = aggregated_data.copy()

    if sort_values:
        plot_series = plot_series.sort_values(ascending=ascending)

    plt.figure(figsize=figsize)
    sns.set_theme(style="whitegrid")

    if orient == "v":
        sns.barplot(
            x=plot_series.index,
            y=plot_series.values,
            palette=color_palette,
            hue=plot_series.index,
            legend=False
        )
        plt.xlabel(xlabel, fontsize=11, labelpad=10)
        plt.ylabel(ylabel, fontsize=11, labelpad=10)
        plt.xticks(rotation=45, ha="right")
    elif orient == "h":
        sns.barplot(
            x=plot_series.values,
            y=plot_series.index,
            palette=color_palette,
            hue=plot_series.index,
            legend=False
        )
        plt.xlabel(ylabel, fontsize=11, labelpad=10)
        plt.ylabel(xlabel, fontsize=11, labelpad=10)
    else:
        raise ValueError("Invalid orientation parameter. Use 'v' for vertical or 'h' for horizontal.")

    plt.title(title, fontsize=14, fontweight="semibold", pad=15)
    plt.grid(axis="y" if orient == "v" else "x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save_path:
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Info] Aggregation chart successfully saved to: {save_path}")

    plt.show()
    plt.close()


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    import numpy as np

    # Generating a dummy synthetic time-series/categorical dataset
    np.random.seed(42)
    date_range = pd.date_range(start="2020-01-01", periods=365 * 3, freq="D")
    
    dummy_df = pd.DataFrame(
        {
            "Consumer_Price_Index": np.cumsum(np.random.normal(0.1, 0.5, len(date_range))) + 100,
            "Market_Region": np.random.choice(["North", "South", "East", "West"], size=len(date_range))
        },
        index=date_range
    )

    # Example 1: Temporal Aggregation (Extracting Year from index tracking)
    dummy_df["Year"] = dummy_df.index.year

    print("--- 1. Computing Temporal Aggregations (Annual Means) ---")
    annual_summary = compute_group_aggregations(
        df=dummy_df,
        group_by_col="Year",
        target_col="Consumer_Price_Index",
        agg_func="mean"
    )
    print(annual_summary)

    print("
--- 2. Rendering Temporal Bar Chart ---")
    plot_aggregation_bars(
        aggregated_data=annual_summary,
        orient="v",
        color_palette="Blues_r",
        title="Annual Average Consumer Price Index Trend",
        xlabel="Calendar Year",
        ylabel="Mean CPI Value"
    )

    # Example 2: Cross-Sectional Categorical Aggregation
    print("
--- 3. Computing Region-Based Aggregations (Median) ---")
    regional_summary = compute_group_aggregations(
        df=dummy_df,
        group_by_col="Market_Region",
        target_col="Consumer_Price_Index",
        agg_func="median"
    )
    print(regional_summary)

    print("
--- 4. Rendering Sorted Horizontal Bar Chart ---")
    plot_aggregation_bars(
        aggregated_data=regional_summary,
        orient="h",
        sort_values=True,
        ascending=False,
        color_palette="viridis",
        title="Median Price Index Across Strategic Regions",
        xlabel="Geographic Region",
        ylabel="Median CPI Value"
    )
