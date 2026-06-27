# Time Series Decomposition Analysis (Additive and Multiplicative EDA)

## 1. Introduction and Purpose
**Time Series Decomposition** is a foundational exploratory data analysis (EDA) technique used to break down an observed time series into its underlying structural components: trend-cycle, seasonality, and irregular residual noise. The primary purpose of this analysis is to isolate these distinct variations to unmask hidden structural changes, detect repetitive seasonal behavior, and strip away high-frequency noise. In data science, machine learning, and econometrics pipelines, decomposition acts as a vital preprocessing and feature engineering step that clarifies whether a series is stationary, uncovers cyclical shifts, and determines whether an additive or multiplicative modeling strategy is optimal for forecasting.

## 2. Background and Motivation
Observed historical time series data often look chaotic and difficult to model directly due to overlapping temporal variations occurring at different frequencies simultaneously. Analyzing these variations in isolation is critical because:
* **Trend Isolation:** It isolates long-term underlying growth or decline patterns, removing short-term noise that can skew macro-level decisions.
* **Seasonality Profiling:** It maps recurring periodic behaviors (e.g., annual consumer price shifts, quarterly revenue jumps, daily traffic spikes) to aid calendar-based adjustments or optimization.
* **Anomalous Signal Detection:** By extracting predictable trend and seasonal patterns, the remaining residuals highlight genuine structural anomalies or random noise components, signaling unexpected external shocks.

## 3. Theoretical Foundation
The classical theory of time series decomposition treats the observed series $Y_t$ as a mathematical combination of three unobserved component series:
1. **Trend-Cycle Component ($T_t$):** The long-term direction of the data, which combines smooth long-term growth/decline (trend) with alternating expansions and contractions (cycles).
2. **Seasonal Component ($S_t$):** A seasonal pattern that repeats at fixed, predictable intervals of time (e.g., daily, weekly, monthly, or annually).
3. **Irregular/Residual Component ($I_t$ or $E_t$):** The remaining random variations or high-frequency noise after trend and seasonal structures are accounted for. This component should ideally resemble white noise.

Decomposition separates these components using moving averages or local regressions (such as STL - Seasonal and Trend decomposition using Loess). Classical decomposition computes moving averages with a window matching the seasonal period to eliminate seasonal cycles and smooth out high-frequency fluctuations, isolating the trend.

## 4. Statistical Concepts and Mathematical Equations
To characterize the relationship among these components, two primary classical mathematical specifications are used:

### A. Additive Decomposition Specification
Used when the amplitude of seasonal fluctuations and irregular variations remains roughly constant, regardless of the level or magnitude of the trend over time.
$$Y_t = T_t + S_t + I_t$$

Where:
* $Y_t$: Observed historical value at time index $t$.
* $T_t$: Estimated trend value at time index $t$.
* $S_t$: Estimated seasonal adjustment factor at time index $t$.
* $I_t$: Irregular residual value at time index $t$.

### B. Multiplicative Decomposition Specification
Used when the seasonal fluctuations change proportionally with the level of the trend series (i.e., if the trend rises, the seasonal swings expand in absolute variance).
$$Y_t = T_t \times S_t \times I_t$$

Alternatively, this can be transformed into an linear additive model by applying a natural logarithm:
$$\ln(Y_t) = \ln(T_t) + \ln(S_t) + \ln(I_t)$$

### C. Moving Average Smoothing for Trend Extraction
For a seasonal period $m$ (e.g., $m=12$ for monthly data), a centered moving average is calculated to eliminate seasonality:
* **If $m$ is even (e.g., 12):** A $2 \times m$-MA is applied to keep the smoothed values centered on actual time steps:
$$\hat{T}_t = \frac{1}{2m} Y_{t-m/2} + \frac{1}{m} \sum_{j=-m/2+1}^{m/2-1} Y_{t+j} + \frac{1}{2m} Y_{t+m/2}$$

## 5. Methodology or Workflow
The systematic execution of a Time Series Decomposition EDA follows these sequential steps:
1. **Datetime Index Validation:** Ensure the data has a strictly ordered datetime or timestamp index with a uniform frequency (e.g., daily, monthly, quarterly).
2. **Imputation & Missing Value Management:** Handle any chronological gaps or missing entries using forward fills, backward fills, or time-based interpolation to guarantee continuous index continuity.
3. **Variance Inspection & Model Selection:** Review an initial time plot of the series. If seasonal variance scales upward as the baseline trends up, select a **multiplicative** model; if seasonal variance is stable, select an **additive** model.
4. **Component Decomposition Extraction:** Apply moving averages or LOESS smoothing algorithms to extract the trend, compute the detrended series, average the detrended values across common sub-periods to extract seasonal components, and subtract/divide both to isolate the residual.
5. **Residual Distribution Analysis:** Evaluate the irregular residuals to check if they conform to white noise (mean centered at 0/1, lacking autocorrelation).
6. **Visualization Output generation:** Build stacked subplots displaying the observed sequence, isolated trend line, repeated seasonal wave, and random residuals together for multi-tier inspection.

## 6. Input Data Requirements
* **Frequency:** Uniformly spaced chronological data (e.g., daily, weekly, monthly, quarterly). Irregularly spaced events must be resampled.
* **Variables:**
  * **Time Reference Index:** A validated pandas DatetimeIndex or consistent monotonic integer sequence.
  * **Target Feature Metric:** Any numerical sequence tracking a single monitored continuous metric (e.g., Consumer Price Index, total sales volume, server load metrics) containing no internal null spaces.
* **Minimum Window Requirements:** The series must contain at least two complete seasonal periods (e.g., $\ge 24$ points for monthly data with an annual cycle) to compute cyclical parameters correctly.

## 7. Expected Outputs and Interpretations
* **Observed Time Chart:** The unaltered history showing overall behavior, structural turning points, and outliers.
* **Trend-Cycle Subplot:** A smoothed long-term curve. If it moves consistently upward or downward, the series has a clear trend, requiring differencing or detrending before applying stationary modeling techniques.
* **Seasonal Subplot:** A highly predictable, perfectly repeating periodic pattern. If its peaks align with specific calendar markers (e.g., November–December retail spikes), it validates calendar-based business explanations.
* **Residual/Irregular Subplot:** The remaining unexplained variations. If significant patterns, waves, or high-variance clusters remain visible here, it indicates that an abrupt structural shock occurred, or that the chosen decomposition frequency/model type did not capture all systematic variations.

## 8. Assumptions and Limitations
* **Static Seasonal Assumptions:** Classical decomposition assumes that the seasonal wave structure remains completely identical year after year. It fails if seasonal habits shift gradually over decades (in such cases, advanced models like STL or SEATS are required).
* **Boundary Data Loss:** Using centered moving averages to extract trends leaves blank gaps at the very beginning and end of the dataset ($m/2$ missing entries on both ends), making real-time endpoint analysis difficult.
* **Sensitivity to Extreme Outliers:** A single extreme historical anomaly can distort the moving average calculation, introducing artificial bumps or dips into the extracted trend line.

## 9. Common Use Cases
* **Economic Indicator Evaluation:** Breaking down foundational indices like the Consumer Price Index (CPI), Gross Domestic Product (GDP), or employment metrics to track fundamental economic growth separate from holiday or weather fluctuations.
* **Retail Demand Planning:** Isolating the true year-over-year operational growth rate of products from high-intensity holiday sales periods.
* **Anomaly Detection Preprocessing:** Removing predictable trends and seasonal cycles to isolate clean residuals, making it easier to flag genuine operational anomalies using statistical control boundaries.

## 10. Advantages and Disadvantages
### Advantages:
* **Highly Interpretive:** Converts a complex single chronological line into intuitive, actionable components that line up with real-world forces (long-term trends vs. short-term seasonal cycles).
* **Automated Feature Engineering:** Simplifies the extraction of explicit trend and seasonal values to use as baseline features in downstream machine learning or regression frameworks.
* **Diagnostic Power:** Quickly identifies whether standard forecasting models will struggle with non-stationary variance trends.

### Disadvantages:
* **Rigid Periodicity Requirements:** Relies on a fixed, pre-specified seasonal cycle frequency integer. It struggles with multi-seasonal datasets (e.g., tracking both hourly and weekly patterns simultaneously) unless specialized tools are used.
* **Endpoint Vulnerability:** Classical calculations cannot extract trend components up to the most recent timestamp due to the trailing width of moving average window boundaries.

## 11. Best Practices and Practical Considerations
* **Log Transforms for Multiplicative Variance:** If the series shows a multiplicative structure, consider taking its natural logarithm. This linearizes the variance, allowing you to use a cleaner additive decomposition framework.
* **Test Residuals for Autocorrelation:** Always plot the Autocorrelation Function (ACF) of the extracted residuals. If strong autocorrelations exist at early lags, it means systematic information is leaking into the residuals instead of being captured by the trend or seasonal components.
* **Choose STL for Dynamic Adjustments:** When dealing with long multi-decade datasets, choose Loess-based decomposition (STL) over classical moving averages. STL allows seasonal patterns to change smoothly over time and protects against outlier distortion.

## 12. Typical Visualizations Associated with the Analysis
* **4-Panel Stacked Decomposition Grid:** A unified grid separating the Observed history, Trend line, Seasonal wave, and Residual scatter.
* **Seasonal Subseries Plot:** Grouping extracted seasonal values by their corresponding sub-period (e.g., plotting all Januarys together, all Februarys together) to check if seasonal behavior is stable over time.
* **Residual Distribution Profile:** Histograms and ACF charts evaluating whether the irregular component is normally distributed and free of serial correlation.