\"\"\"
Time Series Trend Analysis Module
----------------------------------
A reusable, general-purpose implementation for visualizing and exploring 
historical trends, structural movements, and rolling statistics across one 
or more continuous time series variables.
\"\"\"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Union, Optional


def plot_time_series_trends(
    df: pd.DataFrame,
    time_col: Optional[str] = None,
    value_cols: Optional[Union[str, List[str]]] = None,
    rolling_window: Optional[int] = None,
    title: str = "Time Series Trend Analysis",
    x_label: str = "Time",
    y_label: str = "Value",
    figsize: tuple = (12, 6),
    style_dict: Optional[dict] = None
) -> plt.Figure:
    \"\"\"
    Generates a clean, professional time series plot for one or multiple columns, 
    with options for rolling window smoothing to highlight long-term trends.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing temporal and numerical data.
    time_col : str, optional
        The column name containing datetime or temporal sequences. If None, 
        the DataFrame's index is expected to be the temporal index.
    value_cols : str or list of str, optional
        The numerical column(s) to plot over time. If None, all numeric columns 
        in the DataFrame will be plotted.
    rolling_window : int, optional
        The window size for calculating and overlaying a simple moving average trend line.
    title : str, default="Time Series Trend Analysis"
        The title of the generated plot.
    x_label : str, default="Time"
        Label for the horizontal axis.
    y_label : str, default="Value"
        Label for the vertical axis.
    figsize : tuple, default=(12, 6)
        Dimensions of the output figure (width, height).
    style_dict : dict, optional
        Custom styling options mapping column names to line styles (e.g., linestyle, alpha).
        
    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object containing the plot.
    \"\"\"
    # Create a local copy to avoid modifying the original dataframe
    data = df.copy()
    
    # Handle time/index assignment
    if time_col is not None:
        data[time_col] = pd.to_datetime(data[time_col])
        data = data.set_index(time_col)
    else:
        if not isinstance(data.index, pd.DatetimeIndex):
            try:
                data.index = pd.to_datetime(data.index)
            except (ValueError, TypeError):
                # Fallback if index cannot be converted to datetime (e.g., sequential integers)
                pass

    # Handle columns to plot
    if value_cols is None:
        value_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    elif isinstance(value_cols, str):
        value_cols = [value_cols]
        
    if not value_cols:
        raise ValueError("No numeric columns found or specified for time series plotting.")

    # Initialize plot
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)
    
    # Default styling map if none provided
    if style_dict is None:
        style_dict = {}

    # Plot each series
    for col in value_cols:
        if col not in data.columns:
            continue
            
        col_style = style_dict.get(col, {})
        line_style = col_style.get("linestyle", "-")
        alpha = col_style.get("alpha", 0.8)
        linewidth = col_style.get("linewidth", 2.0)
        
        # Plot raw series
        ax.plot(
            data.index, 
            data[col], 
            label=col, 
            linestyle=line_style, 
            alpha=alpha, 
            linewidth=linewidth
        )
        
        # Plot rolling window if specified
        if rolling_window is not None and rolling_window > 1:
            rolling_mean = data[col].rolling(window=rolling_window, center=True).mean()
            ax.plot(
                data.index, 
                rolling_mean, 
                label=f"{col} ({rolling_window}-period SMA)", 
                linestyle=":", 
                alpha=0.9, 
                linewidth=linewidth + 0.5
            )

    # Labeling and polish
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(x_label, fontsize=11, labelpad=10)
    ax.set_ylabel(y_label, fontsize=11, labelpad=10)
    
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none", shadow=False)
    ax.grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Example Demonstration using simulated time series data
    print("Generating simulated time-series data for testing...")
    
    # Generate mock dates and trend metrics
    date_rng = pd.date_range(start="2020-01-01", end="2025-12-31", freq="M")
    np.random.seed(42)
    
    # Create an upward trend with structural variation
    trend_1 = np.linspace(2.0, 4.5, len(date_rng)) + np.random.normal(0, 0.2, len(date_rng))
    # Create a secondary related metric with a seasonal sinusoidal fluctuation
    trend_2 = 3.5 + 0.5 * np.sin(np.linspace(0, 4 * np.pi, len(date_rng))) + np.random.normal(0, 0.15, len(date_rng))
    
    mock_df = pd.DataFrame({
        "Date": date_rng,
        "Primary Indicator": trend_1,
        "Secondary Indicator": trend_2
    })
    
    # Define custom styling parameters for the demonstration
    custom_styles = {
        "Primary Indicator": {"linestyle": "-", "alpha": 0.8},
        "Secondary Indicator": {"linestyle": "--", "alpha": 0.7}
    }
    
    # Call the plotting function
    fig = plot_time_series_trends(
        df=mock_df,
        time_col="Date",
        value_cols=["Primary Indicator", "Secondary Indicator"],
        rolling_window=6,
        title="Simulated Trend Analysis (Primary vs. Secondary Metrics)",
        x_label="Timeline",
        y_label="Index Rate (%)",
        style_dict=custom_styles
    )
    
    # Save the output visualization to verify function capability
    output_image = "time_series_trend_plot.png"
    fig.savefig(output_image, dpi=300)
    print(f"Success! Reusable module verified. Demo plot saved to: {output_image}")
