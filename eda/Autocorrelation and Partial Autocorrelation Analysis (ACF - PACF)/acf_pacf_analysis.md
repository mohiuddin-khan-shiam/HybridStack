# Autocorrelation and Partial Autocorrelation Analysis (ACF / PACF EDA)

## 1. Introduction and Purpose
**Autocorrelation Function (ACF)** and **Partial Autocorrelation Function (PACF)** analyses are core exploratory data analysis (EDA) techniques used to measure and diagnose the linear dependencies within a time series or chronological sequence. The primary purpose of this analysis is to determine how observations at the current time step $t$ are structurally correlated with their own historical past values at prior time steps $t-k$ (lags). Together, ACF and PACF plots serve as a visual guide to evaluate memory persistence, identify seasonal frequencies, confirm data stationarity, and select appropriate lag structures or order hyper-parameters for parametric models like ARIMA or state-space networks.

## 2. Background and Motivation
When dealing with time series sequences, standard independent and identically distributed (i.e.d.) statistical assumptions break down because chronological observations usually carry memory. Analyzing these temporal patterns is critical because:
* **Model Identification:** It provides a direct blueprint for identifying the structure of seasonal patterns and structural parameters in time series models.
* **Stationarity Verification:** It helps visually confirm whether a sequence is stationary (where correlations decay quickly toward zero) or non-stationary (where correlations decay slowly or exhibit strong trend lines).
* **White Noise Diagnostics:** It serves as a tool to check if model forecasting residuals are purely random white noise, confirming whether all structural information has been fully extracted.

## 3. Theoretical Foundation
The theoretical foundation of this analysis rests on **stochastic time series dependency** and **linear prediction filters**. 

* **ACF (Total Correlation):** Measures the absolute linear relationship between a value $Y_t$ and its historical lag $Y_{t-k}$. However, this total correlation includes the indirect compounding effects of intermediate steps ($Y_{t-1}, Y_{t-2}, \dots, Y_{t-k+1}$).
* **PACF (Direct Correlation):** Removes these intermediate effects. It measures the isolated, direct correlation between $Y_t$ and $Y_{t-k}$ after controlling for the linear influence of all shorter lags.

## 4. Statistical Concepts and Mathematical Equations
Let $Y_t$ be a stationary time series with a constant mean $\mu$ and variance $\sigma^2$.

### A. Autocorrelation Function (ACF)
The sample autocorrelation at lag $k$, denoted as $\rho_k$, is defined as the covariance at lag $k$ normalized by the total variance:
$$\rho_k = \frac{\gamma_k}{\gamma_0} = \frac{\sum_{t=k+1}^{N} (Y_t - \mu)(Y_{t-k} - \mu)}{\sum_{t=1}^{N} (Y_t - \mu)^2}$$
Where:
* $\gamma_k$ is the autocovariance at lag $k$.
* $\gamma_0$ is the variance of the series.

### B. Partial Autocorrelation Function (PACF)
The partial autocorrelation at lag $k$, denoted as $\phi_{kk}$, represents the last coefficient of an autoregressive model of order $k$. It isolates the direct relationship by removing intermediate dependencies via linear projection:
$$Y_t = \phi_{k1} Y_{t-1} + \phi_{k2} Y_{t-2} + \dots + \phi_{kk} Y_{t-k} + \epsilon_t$$
The specific coefficient $\phi_{kk}$ can be calculated recursively using the **Durbin-Levinson algorithm**:
$$\phi_{kk} = \frac{\rho_k - \sum_{j=1}^{k-1} \phi_{k-1, j} \rho_{k-j}}{1 - \sum_{j=1}^{k-1} \phi_{k-1, j} \rho_j}$$

### C. Statistical Significance Limits (Confidence Bands)
To evaluate whether a correlation value is statistically meaningful or just random noise, plots include confidence boundaries. Based on Bartlett's formula for a white noise process, the 95% confidence interval is typically calculated as:
$$\pm \frac{1.96}{\sqrt{N}}$$
Where $N$ represents the total number of continuous observations.

## 5. Methodology or Workflow
The systematic execution of an ACF and PACF EDA follows these sequential steps:
1. **Missing Data Cleansing:** Filter out any internal missing or null entries using time-based interpolation or forward fills, as gaps disrupt lag-shifting operations.
2. **Stationarity Check:** Inspect the data's stationarity. If a series has a strong trend, the ACF will decay slowly, making it hard to see other patterns. In these cases, difference the series ($Y_t - Y_{t-1}$) before plotting.
3. **Lag Horizon Setup:** Choose a maximum lag horizon ($K$). A general rule of thumb is to set $K = \min(50, N/4)$ to capture long-term cycles without introducing too much statistical uncertainty at large lags.
4. **Correlation Engine Execution:** Calculate the sample cross-covariances and apply the Durbin-Levinson recursions to compute the full sets of ACF and PACF values.
5. **Diagnostic Visualizations:** Generate stacked subplots containing the correlation bars and their corresponding confidence bands for visual analysis.

## 6. Input Data Requirements
* **Data Typology:** Continuous numerical sequence.
* **Temporal Ordering:** Must be strictly ordered chronologically with a uniform frequency index.
* **Data Volume:** Requires at least $N \ge 30$ data points, but a minimum of 100 observations is recommended to produce reliable, narrow confidence bands.

## 7. Expected Outputs and Interpretations
When analyzing the stacked plots, look for specific correlation signatures to identify the underlying mathematical structure:

| Model Structure | Autocorrelation Function (ACF) | Partial Autocorrelation Function (PACF) |
| :--- | :--- | :--- |
| **Autoregressive (AR - $p$)** | Decays exponentially or as a damped sine wave over time. | Cuts off abruptly to zero after lag step $p$. |
| **Moving Average (MA - $q$)** | Cuts off abruptly to zero after lag step $q$. | Decays exponentially or as a damped sine wave. |
| **Mixed (ARMA - $p, q$)** | Decays exponentially or as a damped sine wave. | Decays exponentially or as a damped sine wave. |
| **Non-Stationary Trend** | Decays extremely slowly, remaining highly significant across many lags. | Displays a dominant lag-1 spike close to 1.0. |
| **Pure White Noise** | All bars fall cleanly within the shaded confidence bands. | All bars fall cleanly within the shaded confidence bands. |

## 8. Assumptions and Limitations
* **Linearity Constraint:** ACF and PACF only measure linear relationships. If the data contains complex non-linear structures or chaotic dependencies, the charts may show no correlation even when a predictable pattern exists.
* **Sensitivity to Non-Stationarity:** Strong underlying trends skew the metrics, causing the ACF plot to stay high across many lags and masking shorter-term seasonal patterns or cycles.
* **Variance Instability:** If the data's volatility changes significantly over time (heteroskedasticity), the confidence bands can become unreliable, leading to false positives.

## 9. Common Use Cases
* **Forecasting Parameter Tuning:** Identifying the structural orders ($p$ and $q$) when configuring ARIMA or SARIMA models.
* **Seasonality Profiling:** Pinpointing recurring spikes at specific seasonal increments (such as lags 12, 24, or 36 for monthly data) to confirm fixed cyclical behaviors.
* **Model Evaluation:** Plotting the errors of a trained model to verify that all historical correlation has been accounted for and that the remaining residuals resemble white noise.

## 10. Advantages and Disadvantages
### Advantages:
* **Clear Model Identification:** Provides a reliable method for separating autoregressive dynamics from moving average structures.
* **Highlights Seasonality:** Makes hidden periodic cycles easy to spot by revealing significant spikes at recurring lag increments.
* **Standardized Assessment:** Provides clear statistical confidence bands to help separate real structural patterns from random background noise.

### Disadvantages:
* **Requires Stationary Input:** Can be difficult to interpret unless the underlying trend is removed first.
* **Limited to Linear Relationships:** Misses more complex, non-linear interactions within the data.

## 11. Best Practices and Practical Considerations
* **Always Analyze ACF and PACF Together:** Looking at only one plot can lead to misidentifying the data's structure (such as confusing an AR process for an MA process).
* **Difference the Series to Reveal Patterns:** If the ACF decays very slowly, apply a first-difference transformation ($Y_t - Y_{t-1}$) and regenerate the plots to expose the underlying short-term dynamics.
* **Watch for Large Lag Noise:** Avoid looking too far out horizontally; correlations calculated at very high lags rely on fewer data points, making them less reliable and harder to interpret.

## 12. Typical Visualizations Associated with the Analysis
* **2-Panel Stacked ACF/PACF Correlation Grid:** Vertical bar plots with shaded significance bands, arranged vertically to simplify structural diagnostics.