"""
Bubble Chart Analysis & Multivariate Relationship Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on multivariate datasets using advanced Bubble Charts. It maps up
to four distinct continuous or categorical variables into a single high-quality 
visualization axis (handling X-position, Y-position, marker size, and color hue) 
while managing scaling, boundary padding, and layout constraints.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_multivariate_bubble_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: str,
    hue_col: str = None,
    title: str = "Multivariate Relationship Profile",
    x_label: str = None,
    y_label: str = None,
    size_label: str = None,
    hue_label: str = None,
    min_marker_size: int = 20,
    max_marker_size: int = 600,
    palette: str = "magma",
    alpha: float = 0.65,
    save_path: str = None
) -> None:
    """
    Generates a professional, publication-ready multivariate bubble chart.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the analysis metrics.
    x_col : str
        Column name to map to the horizontal X-axis.
    y_col : str
        Column name to map to the vertical Y-axis.
    size_col : str
        Column name to map to bubble volume/area. Values must be numeric and positive.
    hue_col : str, optional
        Column name to map to the color channel (supports continuous or categorical data).
    title : str, default="Multivariate Relationship Profile"
        The main descriptive title for the figure.
    x_label : str, optional
        Custom text label for the horizontal X-axis.
    y_label : str, optional
        Custom text label for the vertical Y-axis.
    size_label : str, optional
        Custom label text used in the sizing section of the legend.
    hue_label : str, optional
        Custom label text used in the color section of the legend.
    min_marker_size : int, default=20
        Minimum surface area allocation for the smallest data value.
    max_marker_size : int, default=600
        Maximum surface area allocation for the largest data value.
    palette : str, default="magma"
        The seaborn color map palette used to display continuous or group gradients.
    alpha : float, default=0.65
        Transparency level used to keep overlapping bubbles readable.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    # Build a clean copy containing only the selected columns, dropping any rows with missing data
    required_cols = [x_col, y_col, size_col]
    if hue_col:
        required_cols.append(hue_col)
        
    plot_df = df[required_cols].dropna().copy()
    
    if plot_df.empty:
        raise ValueError("The filtered dataset is empty. Verify that the columns contain valid numerical data.")
        
    # Validate and adjust the size column to prevent negative area rendering
    min_size_val = plot_df[size_col].min()
    if min_size_val <= 0:
        # Shift values up if negative or zero, ensuring all markers have a valid positive size
        offset = abs(min_size_val) + 1.0
        plot_df[size_col] = plot_df[size_col] + offset
        
    # Sort the dataframe in descending order by the size metric
    # This draws smaller bubbles on top of larger ones so they remain visible
    plot_df = plot_df.sort_values(by=size_col, ascending=False)
    
    # Initialize the plot layout using a clean styling preset
    plt.figure(figsize=(11, 7))
    sns.set_theme(style="ticks")
    
    # Generate the primary scatter plot with size and color mapping
    bubble_plot = sns.scatterplot(
        data=plot_df,
        x=x_col,
        y=y_col,
        size=size_col,
        hue=hue_col if hue_col else None,
        sizes=(min_marker_size, max_marker_size),
        palette=palette if hue_col else None,
        alpha=alpha,
        edgecolor="white",
        linewidth=0.8
    )
    
    # Apply labels and titles
    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(x_label if x_label else x_col, fontsize=11, labelpad=8)
    plt.ylabel(y_label if y_label else y_col, fontsize=11, labelpad=8)
    
    plt.grid(True, linestyle=":", alpha=0.5)
    
    # Construct a clean, readable legend layout
    handles, labels = bubble_plot.get_legend_handles_labels()
    
    # Customize legend labels if custom text overrides were provided
    custom_title_mappings = {}
    if hue_col and hue_label:
        custom_title_mappings[hue_col] = hue_label
    if size_label:
        custom_title_mappings[size_col] = size_label
        
    if custom_title_mappings:
        for idx, label in enumerate(labels):
            if label in custom_title_mappings:
                labels[idx] = custom_title_mappings[label]
                
    # Place the updated legend neatly outside or on the margin of the plot area
    plt.legend(
        handles=handles, 
        labels=labels, 
        loc="upper left", 
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0,
        frameon=True,
        facecolor="white"
    )
    
    sns.despine()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    np.random.seed(42)
    n_samples = 80
    
    # Generate mock data simulating core macroeconomic variables
    simulated_gdp = np.random.uniform(1.5, 6.5, size=n_samples)
    # Inflation has a slight negative correlation with GDP in this mock setup
    simulated_inflation = 8.0 - (0.8 * simulated_gdp) + np.random.normal(0, 0.75, size=n_samples)
    # Unemployment serves as the size variable
    simulated_unemployment = np.random.uniform(3.0, 10.0, size=n_samples)
    # Interest rates serve as a secondary color gradient channel
    simulated_rates = (0.5 * simulated_inflation) + (0.3 * simulated_gdp) + np.random.normal(0, 0.2, size=n_samples)
    
    mock_df = pd.DataFrame({
        "Real_GDP": simulated_gdp,
        "Inflation_Rate": simulated_inflation,
        "Unemployment_Rate": simulated_unemployment,
        "Interest_Rate": simulated_rates
    })
    
    print("--- 1. Verification DataFrame ---")
    print(mock_df.head())
    
    print("
--- 2. Launching Bubble Chart Generation ---")
    generate_multivariate_bubble_chart(
        df=mock_df,
        x_col="Real_GDP",
        y_col="Inflation_Rate",
        size_col="Unemployment_Rate",
        hue_col="Interest_Rate",
        title="Macroeconomic Profile Simulation (Bubble Chart EDA)",
        x_label="Real Gross Domestic Product (Growth %)",
        y_label="10-Year Breakeven Inflation Rate (%)",
        size_label="Unemployment Rate (Size Scale)",
        hue_label="Central Bank Interest Rate (%)",
        palette="viridis"
    )