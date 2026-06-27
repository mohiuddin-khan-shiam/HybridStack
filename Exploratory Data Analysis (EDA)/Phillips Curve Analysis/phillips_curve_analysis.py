"""
Phillips Curve Analysis & Bivariate Macroeconomic Relationship Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on bivariate macroeconomic time-series, specifically optimized for
analyzing the Phillips Curve relationship (e.g., Unemployment Rate vs. Inflation Rate).
It handles data preprocessing, stationarity checks, rolling relationship tracking,
lag analysis, and high-quality visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.nonparametric.smoothers_lowess import lowess


def analyze_stationarity(series: pd.Series, name: str) -> dict:
    """
    Performs an Augmented Dickey-Fuller (ADF) test to evaluate stationarity.
    
    Parameters:
    -----------
    series : pd.Series
        The time series data to test.
    name : str
        The name of the variable for reporting purposes.
        
    Returns:
    --------
    dict
        A dictionary containing the ADF statistic, p-value, and stationarity conclusion.
    """
    clean_series = series.dropna()
    result = adfuller(clean_series)
    p_value = result[1]
    is_stationary = p_value < 0.05
    
    return {
        "Variable": name,
        "ADF Statistic": result[0],
        "p-value": p_value,
        "Stationary (alpha=0.05)": is_stationary
    }


def compute_cross_correlations(x: pd.Series, y: pd.Series, max_lags: int = 12) -> pd.Series:
    """
    Computes cross-correlation coefficients between two series across a range of lags.
    Positive lag indicates x leads y; negative lag indicates x lags y.
    
    Parameters:
    -----------
    x : pd.Series
        Independent/lead time series (e.g., Unemployment Rate).
    y : pd.Series
        Dependent/lag time series (e.g., Inflation Rate).
    max_lags : int, default=12
        Maximum number of lags to calculate in both directions.
        
    Returns:
    --------
    pd.Series
        A series indexed by lags with corresponding correlation values.
    """
    lags = range(-max_lags, max_lags + 1)
    correlations = []
    
    for lag in lags:
        if lag < 0:
            corr = x.corr(y.shift(lag))
        elif lag > 0:
            corr = x.shift(lag).corr(y)
        else:
            corr = x.corr(y)
        correlations.append(corr)
        
    return pd.Series(correlations, index=lags)


def plot_bivariate_relationship(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    title: str = "Bivariate Analysis",
    x_label: str = None, 
    y_label: str = None,
    save_path: str = None
) -> None:
    """
    Generates a professional scatter plot with both a linear OLS trendline
    and a non-parametric LOWESS curve to capture potential non-linearities.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the time series.
    x_col : str
        The column name representing the X-axis metric (e.g., Unemployment).
    y_col : str
        The column name representing the Y-axis metric (e.g., Inflation).
    title : str
        The main title for the figure.
    x_label : str, optional
        Custom label for the X-axis.
    y_label : str, optional
        Custom label for the Y-axis.
    save_path : str, optional
        File path to save the generated figure.
    """
    clean_df = df[[x_col, y_col]].dropna().sort_values(by=x_col)
    x_data = clean_df[x_col]
    y_data = clean_df[y_col]
    
    plt.figure(figsize=(9, 7))
    
    # Base scatter plot
    sns.scatterplot(
        x=x_data, 
        y=y_data, 
        alpha=0.55, 
        color="#2b5c8f", 
        edgecolor="w", 
        linewidth=0.5,
        label="Observed Data"
    )
    
    # Linear Regression (OLS) line
    sns.regplot(
        x=x_data, 
        y=y_data, 
        scatter=False, 
        color="#d95f02", 
        line_kws={"linestyle": "--", "linewidth": 1.5},
        label="Linear Trend (OLS)"
    )
    
    # Non-parametric LOWESS curve
    lowess_smoothed = lowess(y_data, x_data, frac=0.6)
    plt.plot(
        lowess_smoothed[:, 0], 
        lowess_smoothed[:, 1], 
        color="#2ca02c", 
        linewidth=2.5, 
        label="LOWESS (Non-linear)"
    )
    
    plt.title(title, fontsize=14, pad=15, fontweight="bold")
    plt.xlabel(x_label if x_label else x_col, fontsize=11)
    plt.ylabel(y_label if y_label else y_col, fontsize=11)
    
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_rolling_relationship(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    window: int = 36,
    title: str = "Rolling Correlation Tracking",
    save_path: str = None
) -> None:
    """
    Plots the rolling correlation coefficient between two variables over time to detect 
    structural modifications or regime shifts.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame with a valid DatetimeIndex.
    x_col : str
        First column name.
    y_col : str
        Second column name.
    window : int, default=36
        Rolling window size (e.g., number of periods/months).
    title : str
        Main title for the figure.
    save_path : str, optional
        File path to save the generated figure.
    """
    rolling_corr = df[x_col].rolling(window=window).corr(df[y_col])
    
    plt.figure(figsize=(11, 5))
    plt.plot(rolling_corr.index, rolling_corr, color="#7570b3", linewidth=2, label=f"{window}-Period Rolling Correlation")
    plt.axhline(0, color="grey", linestyle="--", linewidth=1, alpha=0.7)
    
    plt.title(title, fontsize=13, pad=12, fontweight="bold")
    plt.xlabel("Timeline", fontsize=11)
    plt.ylabel("Pearson Correlation Coefficient", fontsize=11)
    plt.ylim(-1.05, 1.05)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend(loc="lower left")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_cross_correlations(
    ccf_series: pd.Series, 
    title: str = "Cross-Correlation Analysis (Lags)",
    save_path: str = None
) -> None:
    """
    Visualizes the cross-correlations across different lag structures using a professional bar plot.
    
    Parameters:
    -----------
    ccf_series : pd.Series
        Series containing lag steps as index and correlations as values.
    title : str
        Main title for the figure.
    save_path : str, optional
        File path to save the generated figure.
    """
    plt.figure(figsize=(10, 5))
    colors = ["#e31a1c" if val == ccf_series.min() else "#1f78b4" for val in ccf_series.values]
    
    plt.bar(ccf_series.index, ccf_series.values, color=colors, width=0.6, alpha=0.85, edgecolor="black", linewidth=0.5)
    plt.axhline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.5)
    
    # Signify confidence bounds roughly (approximate 2/sqrt(N) rule of thumb if needed)
    plt.title(title, fontsize=13, pad=12, fontweight="bold")
    plt.xlabel("Lag / Lead Step (Negative = X leads Y)", fontsize=11)
    plt.ylabel("Correlation Coefficient", fontsize=11)
    plt.xticks(ccf_series.index)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated macroeconomic framework to verify functionality
    np.random.seed(42)
    dates = pd.date_range(start="2010-01-01", periods=120, freq="M")
    
    # Simulate a structural regime change (traditional curve vs flattening)
    unemployment = np.random.uniform(3.5, 8.0, size=120)
    # Generate inflation with a negative relationship and some noise
    inflation = 12.0 - 1.2 * unemployment + np.random.normal(0, 1.0, size=120)
    
    mock_df = pd.DataFrame({
        "Unemployment_Rate": unemployment,
        "Inflation_Rate": inflation
    }, index=dates)
    
    print("--- Stationarity Assessment ---")
    u_stationarity = analyze_stationarity(mock_df["Unemployment_Rate"], "Unemployment_Rate")
    i_stationarity = analyze_stationarity(mock_df["Inflation_Rate"], "Inflation_Rate")
    print(u_stationarity)
    print(i_stationarity)
    
    print("
--- Plotting Relationships ---")
    plot_bivariate_relationship(
        df=mock_df,
        x_col="Unemployment_Rate",
        y_col="Inflation_Rate",
        title="Phillips Curve Simulation: Inflation vs. Unemployment",
        x_label="Unemployment Rate (%)",
        y_label="Inflation Rate (%)"
    )
    
    plot_rolling_relationship(
        df=mock_df,
        x_col="Unemployment_Rate",
        y_col="Inflation_Rate",
        window=24,
        title="Rolling Macroeconomic Correlation (24-Month Window)"
    )
    
    ccf = compute_cross_correlations(mock_df["Unemployment_Rate"], mock_df["Inflation_Rate"], max_lags=6)
    plot_cross_correlations(ccf, title="Cross-Correlation Function: Unemployment vs Inflation Lags")