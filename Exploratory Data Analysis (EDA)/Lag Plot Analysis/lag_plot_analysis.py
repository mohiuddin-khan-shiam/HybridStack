"""
Lag Plot Analysis & Phase-Space Autocorrelation Profiling Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on sequential time series using Lag Plots. It isolates temporal
dependencies by plotting values at time step (t) against historical states at step (t-k).
It supports multi-lag grid views, trendline overlays, and custom data adjustments
independent of specific project datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_lag_pairs(series: pd.Series, lag: int = 1) -> pd.DataFrame:
    """
    Constructs a paired DataFrame containing the current values (t) and 
    historical shifted values (t-k) for a given lag.
    
    Parameters:
    -----------
    series : pd.Series
        The input numerical time series or sequence.
    lag : int, default=1
        The number of historical steps to look back (k).
        
    Returns:
    --------
    pd.DataFrame
        A DataFrame with two columns: 'Lagged' (Y_{t-k}) and 'Current' (Y_t), 
        with missing values removed.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input 'series' must be a pandas Series object.")
    if lag < 1:
        raise ValueError("Lag parameter must be a positive integer greater than or equal to 1.")
        
    lagged_series = series.shift(lag)
    
    pairs_df = pd.DataFrame({
        "Lagged": lagged_series,
        "Current": series
    })
    
    return pairs_df.dropna()


def plot_single_lag(
    series: pd.Series,
    lag: int = 1,
    title_prefix: str = "Series",
    show_reg_line: bool = True,
    save_path: str = None
) -> None:
    """
    Generates a single high-quality lag plot with an equal aspect ratio 
    and an optional linear trendline.
    
    Parameters:
    -----------
    series : pd.Series
        The input numerical time series or sequence.
    lag : int, default=1
        The historical lookback step to evaluate.
    title_prefix : str, default="Series"
        Descriptive name of the variable under analysis.
    show_reg_line : bool, default=True
        If True, overlays an OLS linear regression line.
    save_path : str, optional
        File system path to save the generated plot.
    """
    pairs_df = generate_lag_pairs(series, lag=lag)
    
    plt.figure(figsize=(7, 7))
    ax = plt.subplot(111)
    
    # Generate scatter plot
    sns.scatterplot(
        data=pairs_df,
        x="Lagged",
        y="Current",
        alpha=0.6,
        color="#2b5c8f",
        edgecolor="w",
        linewidth=0.5,
        ax=ax
    )
    
    # Overlay OLS regression line if requested
    if show_reg_line and not pairs_df.empty:
        sns.regplot(
            data=pairs_df,
            x="Lagged",
            y="Current",
            scatter=False,
            color="#d95f02",
            line_kws={"linestyle": "--", "linewidth": 1.5},
            ax=ax
        )
        
    # Calculate correlation to add to title
    correlation = pairs_df["Lagged"].corr(pairs_df["Current"])
    
    plt.title(f"{title_prefix} Lag Plot (Lag {lag})\nCorrelation: {correlation:.3f}", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel(f"Historical Value (Y_t-{lag})", fontsize=11)
    plt.ylabel("Current Value (Y_t)", fontsize=11)
    
    # Maintain a square aspect ratio so diagonal structures are easy to interpret
    ax.set_aspect("equal", adjustable="datalim")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_lag_grid(
    series: pd.Series,
    lags: list = [1, 2, 3, 4],
    title_prefix: str = "Series",
    save_path: str = None
) -> None:
    """
    Generates a grid layout of lag plots to track how serial correlation 
    changes across different lookback windows.
    
    Parameters:
    -----------
    series : pd.Series
        The input numerical time series or sequence.
    lags : list, default=[1, 2, 3, 4]
        A list of integers representing the lags to include in the grid.
    title_prefix : str, default="Series"
        Descriptive name of the variable under analysis.
    save_path : str, optional
        File system path to save the generated plot grid.
    """
    n_plots = len(lags)
    cols = min(3, n_plots)
    rows = (n_plots + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows), squeeze=False)
    axes = axes.flatten()
    
    for i, lag in enumerate(lags):
        ax = axes[i]
        try:
            pairs_df = generate_lag_pairs(series, lag=lag)
            
            sns.scatterplot(
                data=pairs_df,
                x="Lagged",
                y="Current",
                alpha=0.55,
                color="#1f78b4",
                edgecolor="w",
                linewidth=0.5,
                ax=ax
            )
            
            if not pairs_df.empty:
                sns.regplot(
                    data=pairs_df,
                    x="Lagged",
                    y="Current",
                    scatter=False,
                    color="#e31a1c",
                    line_kws={"linestyle": "--", "linewidth": 1.2},
                    ax=ax
                )
                
            correlation = pairs_df["Lagged"].corr(pairs_df["Current"])
            ax.set_title(f"Lag {lag} (r = {correlation:.2f})", fontsize=11, fontweight="bold")
            
        except Exception as e:
            ax.set_title(f"Lag {lag} - Error", fontsize=11)
            
        ax.set_xlabel(f"Y_t-{lag}")
        ax.set_ylabel("Y_t")
        ax.set_aspect("equal", adjustable="datalim")
        ax.grid(True, linestyle=":", alpha=0.5)
        
    # Hide any unused subplots in the grid boundary
    for j in range(n_plots, len(axes)):
        fig.delaxes(axes[j])
        
    fig.suptitle(f"{title_prefix}: Multi-Lag Spatial Analysis Matrix", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated metrics to verify functionality
    np.random.seed(42)
    n_points = 200
    
    # 1. Generate an Autoregressive (AR1) Process showing strong positive correlation
    ar1_values = np.zeros(n_points)
    for t in range(1, n_points):
        ar1_values[t] = 0.75 * ar1_values[t-1] + np.random.normal(0, 1.0)
    ar1_series = pd.Series(ar1_values, name="AR1_Process")
    
    # 2. Generate a purely random White Noise sequence (no correlation)
    white_noise_series = pd.Series(np.random.normal(0, 1.0, size=n_points), name="White_Noise")
    
    print("--- 1. Evaluating Autoregressive (AR1) Process ---")
    plot_single_lag(ar1_series, lag=1, title_prefix="Simulated AR(1) Signal")
    
    print("\n--- 2. Evaluating Multi-Lag Grid (AR1 Process) ---")
    plot_lag_grid(ar1_series, lags=[1, 2, 3, 6], title_prefix="Simulated AR(1) Signal")
    
    print("\n--- 3. Evaluating Random White Noise Sequence ---")
    plot_single_lag(white_noise_series, lag=1, title_prefix="Simulated White Noise")
"""