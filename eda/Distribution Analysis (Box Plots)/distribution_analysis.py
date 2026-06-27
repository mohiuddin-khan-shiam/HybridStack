"""
Module Name: distribution_analysis.py
Description: A reusable, modular script to perform global distribution analysis
             using box plots, computing exact summary statistics, and identifying 
             numerical outliers across continuous variables.
"""

import os
from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def compute_box_summary_statistics(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> Dict[str, Dict[str, Union[float, List[float]]]]:
    """Calculates box plot summary statistics including quartiles, IQR, and outliers

    for specified numerical columns within a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the numerical data.
    columns : Optional[List[str]], default None
        List of specific column names to analyze. If None, analyzes all numerical columns.

    Returns:
    --------
    Dict[str, Dict[str, Union[float, List[float]]]]
        A nested dictionary mapping column names to their computed statistical parameters:
        {column_name: {min, q1, median, q3, max, iqr, lower_fence, upper_fence, outliers}}
    """
    if columns is None:
        columns = df.select_dtypes(include=["number"]).columns.tolist()

    summary_stats = {}

    for col in columns:
        if col not in df.columns:
            print(f"[Warning] Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Drop missing values for precise calculation
        data_series = df[col].dropna().to_numpy()

        if len(data_series) == 0:
            print(f"[Warning] Column '{col}' contains no valid numerical data. Skipping.")
            continue

        q1, median, q3 = np.percentile(data_series, [25, 50, 75])
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        # Filter points to determine actual non-outlier max and min values
        non_outliers = data_series[
            (data_series >= lower_fence) & (data_series <= upper_fence)
        ]
        actual_min = np.min(non_outliers) if len(non_outliers) > 0 else np.min(data_series)
        actual_max = np.max(non_outliers) if len(non_outliers) > 0 else np.max(data_series)

        # Track outliers explicitly
        outliers = data_series[
            (data_series < lower_fence) | (data_series > upper_fence)
        ].tolist()

        summary_stats[col] = {
            "minimum": float(actual_min),
            "q1_25th": float(q1),
            "median_50th": float(median),
            "q3_75th": float(q3),
            "maximum": float(actual_max),
            "iqr": float(iqr),
            "lower_fence": float(lower_fence),
            "upper_fence": float(upper_fence),
            "outliers_count": len(outliers),
            "outliers": sorted(outliers),
        }

    return summary_stats


def plot_distribution_boxes(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    group_by: Optional[str] = None,
    orient: str = "v",
    title: str = "Distribution Box Plot",
    ylabel: str = "Values",
    xlabel: str = "Features",
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None,
) -> None:
    """Generates and displays a styled box plot for numerical columns.

    Supports single features, multi-feature comparison, and categorical grouping.

    Parameters:
    -----------
    df : pd.DataFrame
        The input data frame matrix.
    columns : Optional[List[str]], default None
        List of target numerical columns to map out.
    group_by : Optional[str], default None
        Categorical column name used to split data into comparative sub-boxes.
    orient : str, default 'v'
        Orientation of the plot: 'v' for vertical boxes, 'h' for horizontal boxes.
    title : str, default 'Distribution Box Plot'
        Plot title text.
    ylabel : str, default 'Values'
        Y-axis label string.
    xlabel : str, default 'Features'
        X-axis label string.
    figsize : tuple, default (10, 6)
        Visual structural dimensions of the output canvas.
    save_path : Optional[str], default None
        System path target to write out the static image asset.
    """
    plt.figure(figsize=figsize)
    sns.set_theme(style="whitegrid")

    if group_by:
        if columns is None or len(columns) == 0:
            raise ValueError("Must specify a target numerical column when using 'group_by'.")
        
        # Plotting a single numeric feature split by categorical column
        sns.boxplot(
            data=df,
            x=group_by if orient == "v" else columns[0],
            y=columns[0] if orient == "v" else group_by,
            orient=orient,
            palette="muted",
            flierprops={"marker": "o", "markerfacecolor": "crimson", "markersize": 5}
        )
        if xlabel == "Features":
            xlabel = group_by
        if ylabel == "Values":
            ylabel = columns[0]
    else:
        # Plotting multiple numeric features side-by-side
        target_columns = columns if columns else df.select_dtypes(include=["number"]).columns.tolist()
        sns.boxplot(
            data=df[target_columns],
            orient=orient,
            palette="Set2",
            flierprops={"marker": "o", "markerfacecolor": "crimson", "markersize": 5}
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
        print(f"[Info] Distribution plot successfully saved to: {save_path}")

    plt.show()
    plt.close()


# ==============================================================================
# Execution Example
# ==============================================================================
if __name__ == "__main__":
    # Generating dummy evaluation dataset representing structural metrics
    np.random.seed(42)
    sample_size = 200

    dummy_df = pd.DataFrame(
        {
            "Indicator_Alpha": np.random.normal(loc=2.5, scale=0.5, size=sample_size),
            "Indicator_Beta": np.random.normal(loc=3.0, scale=1.2, size=sample_size),
            "Category_Group": np.random.choice(["Region_A", "Region_B"], size=sample_size),
        }
    )

    # Injecting visible synthetic outliers
    dummy_df.iloc[0, dummy_df.columns.get_loc("Indicator_Alpha")] = 6.5
    dummy_df.iloc[1, dummy_df.columns.get_loc("Indicator_Alpha")] = -2.0
    dummy_df.iloc[2, dummy_df.columns.get_loc("Indicator_Beta")] = 8.0

    print("--- 1. Computing Distribution Properties ---")
    stats = compute_box_summary_statistics(dummy_df, columns=["Indicator_Alpha", "Indicator_Beta"])
    
    for feature, metrics in stats.items():
        print(f"\nFeature: {feature}")
        print(f"  Median: {metrics['median_50th']:.4f} | IQR: {metrics['iqr']:.4f}")
        print(f"  Fences: [{metrics['lower_fence']:.4f}, {metrics['upper_fence']:.4f}]")
        print(f"  Outliers Flagged Count: {metrics['outliers_count']}")
        print(f"  Outlier Values: {metrics['outliers']}")

    print("\n--- 2. Rendering Multi-Feature Box Plot ---")
    plot_distribution_boxes(
        df=dummy_df,
        columns=["Indicator_Alpha", "Indicator_Beta"],
        title="Comparative Indicator Distribution Analysis",
        ylabel="Percentage (%)",
    )

    print("\n--- 3. Rendering Group-Stratified Box Plot ---")
    plot_distribution_boxes(
        df=dummy_df,
        columns=["Indicator_Beta"],
        group_by="Category_Group",
        title="Beta Indicator Distribution by Regional Categories",
        ylabel="Percentage (%)",
        xlabel="Regions"
    )
