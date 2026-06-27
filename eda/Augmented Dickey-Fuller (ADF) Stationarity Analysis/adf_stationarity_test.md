# Augmented Dickey-Fuller (ADF) Stationarity Analysis (Time Series Unit Root Testing EDA)

## 1. Introduction and Purpose
The **Augmented Dickey-Fuller (ADF) Stationarity Analysis** is a foundational exploratory data analysis (EDA) technique used in statistical time series analysis and econometrics to formally test for the presence of a unit root. Its primary purpose is to determine whether a chronological sequence is **stationary** or **non-stationary**. A stationary time series is one whose statistical properties—such as mean, variance, and autocorrelation structure—do not change over time. In quantitative modeling, predictive analytics, and machine learning pipelines, confirming data stationarity via the ADF test is a critical preprocessing requirement. It dictates whether a raw signal can be modeled directly, or if it must first undergo variance-stabilizing transformations (e.g., differencing or detrending) to avoid spurious regressions and severe model degradation.

## 2. Background and Motivation
Most parametric time series forecasting algorithms (such as ARIMA, Vector Autoregression, and classic linear models) rely heavily on the assumption of weak stationarity. However, real-world data tracking macroeconomic indicators, asset pricing indices, or operational load levels frequently exhibit stochastic trends or random walks. Analyzing time series via formal unit root testing is critical because:
* **Spurious Regression Mitigation:** Regressing a non-stationary variable against another can show a deceptively high $R^2$ value and highly significant coefficients even when the two variables have zero structural connection.
* **Variance Boundary Definition:** Non-stationary processes have a time-dependent variance that grows toward infinity as time progresses, making long-term statistical inferences and prediction intervals highly unreliable.
* **Transformation Architecture Blueprint:** The test result provides a rigorous mathematical reason to apply mathematical transformations like first-differencing ($\Delta Y_t = Y_t - Y_{t-1}$) or structural log adjustments before training downstream models.

## 3. Theoretical Foundation
The theoretical core of the ADF test rests on the mathematical behavior of **Autoregressive (AR)** processes. Consider a basic first-order autoregressive model, $	ext{AR}(1)$:
$$Y_t = \phi Y_{t-1} + \epsilon_t$$
Where $\epsilon_t$ represents white noise errors. The stationarity of this system depends entirely on the coefficient $\phi$:
1. If $|\phi| < 1$, the process is stationary, and shocks or external disturbances gradually fade away over time, allowing the system to revert to its mean.
2. If $\phi = 1$, the process contains a **Unit Root** (a random walk). Shocks have a permanent, cumulative impact on the series, and the variance expands continuously.

To simplify estimation, the equation is rewritten by subtracting $Y_{t-1}$ from both sides, shifting the evaluation to a parameter $\gamma$:
$$\Delta Y_t = (\phi - 1) Y_{t-1} + \epsilon_t = \gamma Y_{t-1} + \epsilon_t$$
Testing for a unit root ($\phi = 1$) is thus mathematically equivalent to testing whether the parameter $\gamma = 0$.

## 4. Statistical Concepts and Mathematical Equations
The Augmented Dickey-Fuller test expands upon the basic $	ext{AR}(1)$ test framework by adding lagged differences of the dependent variable. This adjustment controls for higher-order serial correlation in the error term, preventing it from biasing the test results.

### A. General ADF Regression Models
The test evaluates $\gamma$ by fitting one of three structural ordinary least squares (OLS) regression models, depending on whether the data exhibits a baseline intercept or a deterministic trend:
1. **Model with No Intercept and No Deterministic Trend:**
   $$\Delta Y_t = \gamma Y_{t-1} + \sum_{i=1}^{p} eta_i \Delta Y_{t-i} + \epsilon_t$$
2. **Model with an Intercept (Drift Constant $lpha_0$):**
   $$\Delta Y_t = lpha_0 + \gamma Y_{t-1} + \sum_{i=1}^{p} eta_i \Delta Y_{t-i} + \epsilon_t$$
3. **Model with an Intercept and a Deterministic Linear Trend ($lpha_1 t$):**
   $$\Delta Y_t = lpha_0 + lpha_1 t + \gamma Y_{t-1} + \sum_{i=1}^{p} eta_i \Delta Y_{t-i} + \epsilon_t$$
Where $p$ represents the maximum number of historical lag intervals included to account for serial correlation.

### B. Hypothesis Formulations
* **Null Hypothesis ($H_0$):** $\gamma = 0$ (or equivalently, $\phi = 1$). The series possesses a unit root and is **non-stationary**. It exhibits stochastic trend behavior.
* **Alternative Hypothesis ($H_a$):** $\gamma < 0$ (or equivalently, $\phi < 1$). The series does not possess a unit root and is **stationary**. It tends to revert to its mean or deterministic trend line.

### C. Test Statistic calculation
The ADF test statistic is the t-ratio calculated for the estimated parameter $\gamma$:
$$t_{\gamma} = rac{\hat{\gamma}}{	ext{SE}(\hat{\gamma})}$$
Because this regression violates traditional stationary assumptions under the null hypothesis, $t_{\gamma}$ does not follow a standard Student's t-distribution. Instead, it is compared against specific empirical critical values compiled via Monte Carlo simulations, known as the **Dickey-Fuller Critical Values Tables**.

## 5. Methodology or Workflow
The systematic execution of an ADF Stationarity Analysis EDA follows these sequential steps:
1. **Chronological Index Cleansing:** Validate that the target array is chronologically sorted with a uniform time frequency index.
2. **Missing Data Removal:** Strip out any missing entries or leading/trailing null blocks, as unit root regressions require unbroken historical segments.
3. **Regression Specification Selection:** Determine whether to include a constant intercept, or both an intercept and a linear trend, based on a visual inspection of the raw time plot.
4. **Lag Length Selection ($p$):** Select an optimal lag length to filter out serial correlation without overfitting. This is typically automated using information criteria like the Akaike Information Criterion (AIC) or Bayesian Information Criterion (BIC).
5. **Statistical Regression Execution:** Run the ADF OLS matrix solver to compute the test statistic, empirical p-value, and critical values thresholds.
6. **Hypothesis Evaluation:** Compare the calculated test statistic and p-value against the critical thresholds to choose whether to reject the null hypothesis.
7. **Transformation Iteration:** If the test fails to reject the null hypothesis (confirming the series is non-stationary), apply a first-difference transformation and re-test to see if the transformed data achieves stationarity.

## 6. Input Data Requirements
* **Data Format:** Single continuous numerical vector or a 1D column from a tabular dataset.
* **Index Configuration:** Must be ordered sequentially. While a pandas DatetimeIndex is preferred, a stable, monotonic integer index is acceptable.
* **Data Volume:** Requires a minimum sample size of $N \ge 30$ records, though over 100 observations is highly recommended to ensure the test has sufficient statistical power to correctly reject a false null hypothesis.

## 7. Expected Outputs and Interpretations
* **ADF Test Statistic Score:** A negative continuous value. To reject the null hypothesis, this score must be **more negative** (smaller) than the empirical critical values ($1\%$, $5\%$, or $10\%$) listed in the Dickey-Fuller tables.
* **Calculated p-value:** A probability bound between $0$ and $1$. If the p-value sits safely below your chosen significance level (typically $lpha = 0.05$), you reject the null hypothesis and conclude that the series is stationary.
* **Actionable Transformation Blueprint:** * If $p < 0.05 \implies$ **Stationary:** The series is ready for direct autoregressive or machine learning modeling.
  * If $p \ge 0.05 \implies$ **Non-Stationary:** The series requires transformation. Apply a first-difference step ($\Delta Y_t$) or remove the deterministic trend before modeling.

## 8. Assumptions and Limitations
* **Linearity Restriction:** The ADF test assumes the underlying data generation process is linear. If the time series is governed by complex non-linear trends, threshold breaks, or chaotic attractors, the test can mistake these behaviors for a unit root, leading to false negatives.
* **Low Statistical Power Against Near-Unit Roots:** The test struggles to differentiate between a true random walk ($\phi = 1.0$) and a stationary process with high persistence (e.g., $\phi = 0.98$). It frequently misclassifies these highly persistent series as non-stationary, especially in small sample sizes.
* **Vulnerability to Structural Breaks:** If a time series experiences a permanent, sudden structural break (such as a baseline shift due to a policy change), the standard ADF test can easily misinterpret this shift as a unit root, incorrectly concluding that the data is non-stationary.

## 9. Common Use Cases
* **Forecasting Pipeline Pre-validation:** Testing numerical features before configuring models like ARIMA or Vector Autoregression to ensure the input data meets mandatory stationarity assumptions.
* **Financial Pairs Trading Research:** Testing the residuals of a spread between two highly correlated assets to confirm cointegration, revealing a stationary mean-reverting relationship that can be traded.
* **Macroeconomic Feature Engineering:** Screening foundational economic variables (such as inflation rates, interest rates, or GDP indices) to identify which metrics require differencing transformations before being used in predictive models.

## 10. Advantages and Disadvantages
### Advantages:
* **Rigorous Mathematical Foundation:** Replaces subjective visual interpretations of time plots with clear, mathematically sound hypothesis boundaries and confidence thresholds.
* **Flexible Lag Configurations:** Natively adjusts lag horizons to filter out complex serial correlation in the error terms, preventing biased results.
* **Industry-Wide Standardization:** Operates as a universally accepted baseline test for stationarity across data science, academic econometrics, and quantitative finance.

### Disadvantages:
* **Prone to False Negatives:** Frequently fails to correctly identify stationarity in highly persistent series or small datasets.
* **Distorted by Structural Breaks:** Sudden, permanent shifts in the data's baseline can artificially inflate the test's non-stationarity findings.

## 11. Best Practices and Practical Considerations
* **Always Visualize the Data First:** Never rely purely on the numeric test score; always plot the raw time series to see if it exhibits a visible linear trend, which will guide your choice of regression model (e.g., setting `regression='ct'`).
* **Use Automated Lag Selection:** Rely on verified criteria like the Akaike Information Criterion (`maxlag=None, autolag='AIC'`) to let the algorithm automatically find the optimal balance between lag coverage and model complexity.
* **Re-test After Differencing:** If the raw data is non-stationary, apply a first difference, strip out the resulting null boundaries, and re-run the ADF test to confirm that your transformation successfully achieved stationarity.

## 12. Typical Visualizations Associated with the Analysis
* **Observed Time Plot with Highlighted Mean:** A chronological line plot overlaid with a global average line, helping you see if the data naturally drifts away from its baseline or exhibits time-varying variance.
* **Differenced Transformation Comparison:** A two-panel stacked layout showing the raw non-stationary data in the top panel and the clean, stationary differenced series underneath to demonstrate the effect of the transformation.