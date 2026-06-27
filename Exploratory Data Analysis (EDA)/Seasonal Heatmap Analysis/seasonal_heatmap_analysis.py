"""
Seasonal Heatmap Analysis & Chronological Grid Layout Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time series sequences using two-dimensional matrix heatmaps.
It specializes in segmenting, pivoting, and scaling target metrics across dual temporal
dimensions (such as Year vs. Month or Day vs. Hour) to expose underlying cyclical patterns,
long-term structural trends, and anomalies independent of specific project datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_seasonal_matrix(
    df: pd.DataFrame,
    target_col: str,
    macro_period: str = "year",
    micro_period: str = "month",
    agg_func: str = "mean"
) -> pd.DataFrame:
    """
    Extracts time features from a DatetimeIndex and builds a pivoted data matrix 
    for heatmap visualization.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with a valid pandas DatetimeIndex.
    target_col : str
        The name of the column to aggregate and display in the grid cells.
    macro_period : str, default="year"
        The datetime component for columns ('year', 'quarter', 'month').
    micro_period : str, default="month"
        The datetime component for rows ('month', 'dayofweek', 'hour').
    agg_func : str, default="mean"
        The aggregation method used for overlapping cells ('mean', 'sum', 'median').
        
    Returns:
    --------
    pd.DataFrame
        A pivoted matrix DataFrame ready for heatmap rendering.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("The input DataFrame must have a valid pandas DatetimeIndex.")
        
    working_df = df[[target_col]].copy()
    
    # Extract macro-chronological column properties
    if macro_period == "year":
        working_df["_Macro"] = working_df.index.year
    elif macro_period == "quarter":
        working_df["_Macro"] = working_df.index.quarter
    elif macro_period == "month":
        working_df["_Macro"] = working_df.index.month
    else:
        raise ValueError(f"Unsupported macro_period: {macro_period}")
        
    # Extract micro-cyclical row properties
    if micro_period == "month":
        working_df["_Micro"] = working_df.index.month
    elif micro_period == "dayofweek":
        working_df["_Micro"] = working_df.index.dayofweek + 1  # Standardize to 1-7 layout
    elif micro_period == "hour":
        working_df["_Micro"] = working_df.index.hour
    else:
        raise ValueError(f"Unsupported micro_period: {micro_period}")
        
    # Build the pivoted structural matrix
    pivoted_matrix = working_df.pivot_table(
        values=target_col,
        index="_Micro",
        columns="_Macro",
        aggfunc=agg_func
    )
    
    return pivoted_matrix


def plot_seasonal_heatmap(
    matrix_df: pd.DataFrame,
    title: str = "Chronological Trend Heatmap",
    x_label: str = "Macro Dimension",
    y_label: str = "Micro Dimension",
    cbar_label: str = "Metric Value",
    cmap: str = "coolwarm",
    annotate: bool = True,
    value_format: str = ".1f",
    save_path: str = None
) -> None:
    """
    Renders a high-quality, professional two-dimensional seasonal heatmap grid.
    
    Parameters:
    -----------
    matrix_df : pd.DataFrame
        The pivoted data matrix from generate_seasonal_matrix.
    title : str, default="Chronological Trend Heatmap"
        The main descriptive title for the figure.
    x_label : str, default="Macro Dimension"
        Text label for the horizontal axis.
    y_label : str, default="Micro Dimension"
        Text label for the vertical axis.
    cbar_label : str, default="Metric Value"
        The descriptive label attached to the color bar scale indicator.
    cmap : str, default="coolwarm"
        The color mapping palette name (e.g., 'coolwarm', 'viridis', 'YlGnBu').
    annotate : bool, default=True
        If True, prints the aggregated values inside the grid cells.
    value_format : str, default=".1f"
        The Python formatting string for cell text labels (e.g., '.0f', '.2f').
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    plt.figure(figsize=(14, 7))
    
    # Generate the heatmap grid layout
    sns.heatmap(
        matrix_df,
        cmap=cmap,
        annot=annotate,
        fmt=value_format,
        linewidths=0.4,
        linecolor="#dcdcdc",
        cbar_kws={"shrink": 0.85, "label": cbar_label},
        robust=True
    )
    
    # Configure titles and labels
    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(x_label, fontsize=11, labelpad=10)
    plt.ylabel(y_label, fontsize=11, labelpad=10)
    
    # Clean up axis ticks for better readability
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated time series dataset to verify functionality
    np.random.seed(42)
    time_horizon = pd.date_range(start="2018-01-01", periods=72, freq="M")
    
    # Simulate a steady upward trend combined with clear annual seasonality
    underlying_trend = np.linspace(200, 280, 72)
    # Seasonal effect: peak demand in summer months (index positions 5, 6, 7)
    seasonal_factors = 15 * np.sin(2 * np.pi * np.arange(72) / 12)
    stochastic_noise = np.random.normal(0, 3, size=72)
    
    mock_values = underlying_trend + seasonal_factors + stochastic_noise
    
    mock_df = pd.DataFrame({
        "Simulated_Index": mock_values
    }, index=time_horizon)
    
    print("--- 1. Generating Matrix Layout (Year vs. Month) ---")
    pivoted_grid = generate_seasonal_matrix(
        df=mock_df,
        target_col="Simulated_Index",
        macro_period="year",
        micro_period="month",
        agg_func="mean"
    )
    print("Pivoted structural matrix preview:")
    print(pivoted_grid.head())
    
    print("
--- 2. Visualizing Seasonal Heatmap Layout ---")
    plot_seasonal_heatmap(
        matrix_df=pivoted_grid,
        title="Simulated Trend Heatmap: Multi-Year Seasonal Profile",
        x_label="Calendar Year",
        y_label="Month of Year",
        cbar_label="Index Metric Units",
        cmap="coolwarm",
        value_format=".0f"
    )