# Lag Plot Analysis (Autocorrelation and Phase-Space Profile EDA)

## 1. Introduction and Purpose
A **Lag Plot** is a specialized exploratory data analysis (EDA) technique for time series and sequential datasets. Its primary purpose is to check for the presence of linear or non-linear serial dependency (autocorrelation), cyclical rhythms, deterministic trends, or random walk structures by plotting observations at time step $t$ against their historical values shifted by a specific lag window $k$ (time step $t-k$). In data science and forecasting pipelines, this bivariate visualization acts as a reliable pre-modeling filter. It helps determine if a sequence is truly random (white noise) or if it possesses an internal historical memory that can be modeled using autoregressive (AR) or machine learning frameworks.

## 2. Background and Motivation
When dealing with sequential or time series data, standard descriptive summaries (like the mean, median, or variance) often fail to capture how individual data points depend on their chronological ordering. Analyzing these sequential relationships with lag plots is critical because:
* **Memory Identification:** It provides a visual check to see if a value's current state is tied to its recent history, helping you select the right feature lags for modeling.
* **Randomness Testing:** It visually verifies whether a dataset is truly random (independent and identically distributed - i.e., white noise), which is an essential test for validating model residuals.
* **Non-Linear Dynamics Mapping:** Unlike structural correlation matrices, a lag plot maps data in a two-dimensional phase-space, allowing you to visually spot complex, non-linear relationships, thresholds, or chaotic attractors.

## 3. Theoretical Foundation
The theoretical core of lag plot analysis rests on **stochastic dependencies** and **phase-space reconstruction**. Traditional statistical models require independent observations. Time series data, however, often violates this rule through a property called **serial correlation**, where past values influence future outcomes.

A lag plot maps a single chronological sequence into a two-dimensional phase space defined by the coordinates $(Y_{t-k}, Y_t)$. If the underlying process is completely random, the data points will scatter evenly across the grid without forming a distinct shape. If the data follows a systematic process, the points will form a structured shape (such as a diagonal line, ellipse, or curve) that reflects the mathematical relationship between the past and present.

## 4. Statistical Concepts and Mathematical Equations
Let $Y = \{Y_1, Y_2, \dots, Y_N\}$ represent a chronologically sorted sequence of observations. For a chosen integer lag $k \ge 1$, we construct a set of paired coordinates:
$$\left(Y_{t-k}, Y_tight) \quad 	ext{for } t = k+1, k+2, \dots, N$$

### A. Linear Correlation Structure
If a linear relationship dominates the lag plot, it directly mirrors the classical **Autocorrelation Coefficient ($ho_k$)** at lag $k$:
$$ho_k = rac{\sum_{t=k+1}^{N} (Y_t - \mu)(Y_{t-k} - \mu)}{\sum_{t=1}^{N} (Y_t - \mu)^2}$$
Where $\mu$ represents the global mean of the series.

### B. Structural Interpretations of Lag Geometries
The shape and distribution of points on a lag plot reveal specific structural behaviors:
1. **Positive Linear Structure:** Points cluster tightly along a bottom-left to top-right diagonal line ($Y_t = eta_0 + eta_1 Y_{t-k} + \epsilon_t$ where $eta_1 > 0$). This indicates a strong positive autocorrelation, where high values tend to be followed by high values, and low values by low values.
2. **Negative Linear Structure:** Points cluster along a top-left to bottom-right diagonal line ($eta_1 < 0$). This indicates negative autocorrelation, where high values alternate with low values.
3. **Circular or Elliptical Ring Structure:** Points form a circular or elliptical pattern. This indicates strong periodic cycles or seasonality in the data, where the shape's width depends on how closely the chosen lag matches the length of the cycle.
4. **Uniform Dispersion (No Structure):** Points spread out evenly in a random cloud. This indicates that the sequence lacks serial correlation at that lag and resembles white noise.

## 5. Methodology or Workflow
The systematic execution of a Lag Plot Analysis EDA follows these sequential steps:
1. **Sequence Sorting:** Ensure the target vector is sorted in exact chronological order, with no missing dates or broken intervals.
2. **Lag Parameter Assignment:** Define the target lookback step $k$. Usually, a primary plot checks lag $1$ ($Y_{t-1}$ vs. $Y_t$) to spot immediate momentum, followed by checks at seasonal increments (e.g., lag 12 for monthly data) to detect recurring periodic patterns.
3. **Coordinate Alignment:** Shift the data vector by the lookback window $k$ to pair past values ($Y_{t-k}$) with their corresponding current values ($Y_t$).
4. **Phase-Space Plotting:** Generate a scatter plot using the paired coordinates, keeping the aspect ratio square (1:1) so diagonal trends are easy to read.
5. **Trendline Overlay:** Fit an OLS regression line or a non-parametric smoother over the scatter points to help identify the underlying direction and strength of the relationship.

## 6. Input Data Requirements
* **Data Typology:** A continuous numerical sequence.
* **Index Requirements:** Strictly ordered chronological indexes or monotonic integer positions.
* **Data Volume:** While a lag plot can be generated with as few as 30 points, having at least 100 observations helps make structural patterns and shapes stand out clearly against noise.

## 7. Expected Outputs and Interpretations
* **Diagonal Oval Pattern:** Confirms a strong trend or highly persistent autoregressive memory. If the data is non-stationary, the points will stretch out into a long diagonal line across the plot.
* **Sinusoidal/Cyclical Rings:** Reveals hidden seasonality. If you increase the lookback window $k$ and the ring collapses into a tight diagonal line, it means the chosen lag matches the exact length of the seasonal cycle (e.g., a 12-month lag on annual economic data).
* **Random Cloud:** Indicates an unpredictable white noise sequence, meaning past values provide no helpful information for predicting future steps at that specific lag.

## 8. Assumptions and Limitations
* **Vulnerability to Long-Term Trends:** If a time series has a strong, dominating long-term trend, a lag-1 plot will always show a tight diagonal line. This can hide more subtle, short-term cyclical interactions or seasonal variations.
* **Single Lag per Axis:** Each plot can only check one lookback step $k$ at a time. To evaluate multiple historical dependencies simultaneously, you need to use an Autocorrelation Function (ACF) chart or generate a grid of multiple lag plots.
* **Sensitivity to Scale:** Extreme historical anomalies or large data spikes can expand the plot boundaries, compress the core data points into a tight cluster, and make the overall relationship harder to read.

## 9. Common Use Cases
* **Forecasting Feasibility Pre-checks:** Evaluating time series data before modeling to confirm it has enough internal memory to support autoregressive forecasting techniques (like ARIMA or LSTM).
* **Model Residual Diagnostics:** Plotting a model's prediction errors to verify they form a completely random cloud. If any structure or pattern remains, it signals that the model missed a systematic relationship.
* **Macroeconomic Regime Analysis:** Studying metrics like inflation rates, GDP indexes, or asset returns to identify long-term persistence and structural economic cycles.

## 10. Advantages and Disadvantages
### Advantages:
* **Identifies Non-Linear Patterns:** Captures complex, non-linear relationships and thresholds that standard correlation coefficients can miss.
* **Simple and Intuitive:** Provides a quick, clear visual check for randomness without requiring complex statistical calculations.
* **No Rigid Modeling Rules:** Operates as a non-parametric exploration tool that does not assume the data follows a specific distribution.

### Disadvantages:
* **Qualitative Insights:** Offers visual descriptions rather than exact numerical measurements of correlation strength.
* **Requires Multiple Plots:** Needs separate plots for each lag step, which can create visual clutter when checking long historical horizons.

## 11. Best Practices and Practical Considerations
* **Use Differenced Data to Uncover Cycles:** If a strong, dominant trend obscures your view, try differencing the series ($Y_t - Y_{t-1}$) before plotting to remove the trend and expose underlying seasonal patterns or cycles.
* **Maintain a Square Aspect Ratio:** Always set your plot's aspect ratio to 1:1 (`ax.set_aspect('equal')`) so that positive and negative 45-degree trends are easy to spot and compare accurately.
* **Combine with ACF and PACF Charts:** Use lag plots alongside Autocorrelation (ACF) and Partial Autocorrelation (PACF) plots to back up your visual insights with precise statistical metrics.

## 12. Typical Visualizations Associated with the Analysis
* **Bivariate Lag Scatter Plot:** The standard layout plotting $Y_{t-k}$ against $Y_t$ with an equal aspect ratio.
* **Multi-Lag Diagnostic Grid:** A multi-panel grid displaying lag-1, lag-2, lag-3, and seasonal lag steps side-by-side to track how memory fades over time.