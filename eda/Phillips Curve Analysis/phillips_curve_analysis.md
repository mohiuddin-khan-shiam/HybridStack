# Phillips Curve Analysis (Bivariate Macroeconomic Relationship EDA)

## 1. Introduction and Purpose
The **Phillips Curve Analysis** is a foundational exploratory data analysis (EDA) technique used in macroeconomics and financial econometrics to examine the empirical relationship between inflation and unemployment. The primary purpose of this analysis is to evaluate whether an economy exhibits the traditional inverse relationship between labor market slack (unemployment) and price/wage inflation, or if the relationship has evolved into a structural break, stagflationary pattern, or a flattened regime. In a data science and predictive modeling context, this bivariate EDA establishes baseline cross-correlations, identifies lag structures, detects structural anomalies, and informs feature engineering for forecasting models.

## 2. Background and Motivation
Introduced by A.W. Phillips in 1958 based on UK historical data, the original hypothesis suggested an exploitable trade-off for policymakers: lower unemployment could be achieved at the cost of higher inflation. In modern economic data analysis, analyzing this relationship is critical because:
* **Regime Identification:** It determines whether the historical macroeconomic trade-off holds true for a given historical window or specific economic region.
* **Monetary Policy Signatures:** It exposes how central bank interventions (e.g., quantitative easing, rate hikes) disrupt or reinforce the correlation.
* **Feature Selection:** It evaluates whether unemployment metrics serve as a reliable leading, lagging, or coincident indicator for inflationary pressures.

## 3. Theoretical Foundation
The classical Phillips Curve posits an inverse, non-linear relationship between unemployment and inflation. In modern macroeconomics, this has evolved into the **Expectations-Augmented Phillips Curve** (associated with Milton Friedman and Edmund Phelps) and the **New Keynesian Phillips Curve (NKPC)**, which incorporates rational expectations and forward-looking behavior.

From an exploratory standpoint, the analysis tests whether:
1. Short-run trade-offs exist (negative slope).
2. The long-run relationship is vertical at the Non-Accelerating Inflation Rate of Unemployment (NAIRU).
3. The relationship has experienced "flattening" due to structural forces like globalization, anchored expectations, or labor market digitization.

## 4. Statistical Concepts and Mathematical Equations
To quantify the relationship during EDA, several statistical formulations are applied:

### A. Linear Specification
A simple baseline ordinary least squares (OLS) representation:
<div style="text-align:center; margin:1em 0; font-size:1.1em;">
  <span class="math">π<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub> U<sub>t</sub> + ε<sub>t</sub></span>
</div>
Where:
* <span class="math">π<sub>t</sub></span>: Inflation rate at time *t* (e.g., CPI change, Core PCE, or 10-Year Breakeven Inflation Rate).
* <span class="math">U<sub>t</sub></span>: Unemployment rate at time *t*.
* <span class="math">β<sub>1</sub></span>: The slope coefficient. The traditional theory implies <span class="math">β<sub>1</sub> < 0</span>.
* <span class="math">ε<sub>t</sub></span>: Stochastic error term.

### B. Expectations-Augmented Specification
Incorporating expected inflation or historical inertia:
<div style="text-align:center; margin:1em 0; font-size:1.1em;">
  <span class="math">π<sub>t</sub> = π<sub>t</sub><sup>e</sub> - γ(U<sub>t</sub> - U<sup>*</sup>) + ε<sub>t</sub></span>
</div>
Where:
* <span class="math">π<sub>t</sub><sup>e</sup></span>: Expected inflation.
* <span class="math">U<sup>*</sup></span>: The Natural Rate of Unemployment or NAIRU.
* <span class="math">γ</span>: Sensitvity parameter parameter (<span class="math">γ > 0</span>).

### C. Correlation and Cross-Correlation Metrics
Because macroeconomic impacts are rarely instantaneous, we evaluate the Cross-Correlation Function (CCF) at lag *k*:
<div style="text-align:center; margin:1em 0; font-size:1.1em;">
  <span class="math">ρ<sub>xy</sub>(k) = E[(X<sub>t</sub> - μ<sub>x</sub>)(Y<sub>t+k</sub> - μ<sub>y</sub>)] / (σ<sub>x</sub> σ<sub>y</sub>)</span>
</div>

## 5. Methodology or Workflow
The systematic execution of a Phillips Curve EDA follows these sequential steps:
1. **Time-Series Alignment:** Sync the inflation series (e.g., monthly/quarterly) with the unemployment rate series using consistent timestamps.
2. **Stationarity Assessment:** Evaluate both series using the Augmented Dickey-Fuller (ADF) test to identify if they are stationary <span class="math">I(0)</span> or integrated <span class="math">I(1)</span>.
3. **Bivariate Scatter Analysis:** Plot inflation against unemployment to visually inspect linear or non-linear patterns, clusters, and extreme outliers.
4. **Rolling Correlation & Regime Detection:** Compute rolling Pearson/Spearman coefficients over fixed windows (e.g., 36-month, 60-month) to determine if the relationship is stable or time-varying.
5. **Lagged Correlation Evaluation:** Compute and visualize cross-correlations across multiple lags to determine if unemployment leads or lags inflation.
6. **Local Polynomial Smoothing (Lowess):** Apply a non-parametric local regression to trace the empirical curve without assuming strict linearity.

## 6. Input Data Requirements
* **Frequency:** Uniformly sampled time-series data (typically monthly or quarterly).
* **Variables:**
  * **Unemployment Metric:** Labor underutilization rate (e.g., U3 or U6 rate), expressed as a percentage.
  * **Inflation Metric:** Price index changes (e.g., YoY Core CPI, Core PCE) or market-based forward indicators (e.g., 5-Year or 10-Year Breakeven Inflation Rates), expressed as a percentage.
* **Format:** A tabular format (e.g., pandas DataFrame) with a validated datetime index and no missing structural intervals.

## 7. Expected Outputs and Interpretations
* **Scatter Plot with Regression Line:** A negative slope confirms a traditional short-run trade-off. A flat or horizontal line suggests a structural break where inflation became decoupled from domestic labor market tightness.
* **Rolling Correlation Series:** Shifts from negative to positive correlations signal macroeconomic structural shocks (e.g., supply-side shocks like the 1970s oil crisis, or the post-2010 secular stagnation).
* **Cross-Correlation Matrix/Plot:** Identifies the optimal structural lag. For instance, if the strongest negative correlation occurs at lag -6, it implies that changes in unemployment take approximately 6 months to manifest in inflation adjustments.

## 8. Assumptions and Limitations
* **Supply-Side Blindness:** The bivariate Phillips Curve implicitly assumes demand-driven economic fluctuations. It fails during supply shocks (e.g., commodity bottlenecks), which cause both inflation and unemployment to rise simultaneously (stagflation).
* **Non-Stationarity Risks:** Macroeconomic time-series often exhibit trends. Correlating non-stationary series can yield spurious regressions unless proper differencing or detrending (e.g., Hodrick-Prescott filter) is applied.
* **Omitted Variable Bias:** The simple curve ignores critical variables such as global supply chain pressure indices, monetary velocity, and fiscal impulse indicators.

## 9. Common Use Cases
* **Macroeconomic Risk Assessment:** Central banks and asset management firms utilize this analysis to gauge overheating or slack within an economy.
* **Feature Engineering for Predictive Models:** Identifying the optimal historical lag helps build accurate multi-step ahead forecasting models (e.g., VAR, LSTM, Prophet).
* **Regime Switching Pre-processing:** Identifying structural breakdown points provides logic for training multi-regime models (e.g., Markov Switching Models).

## 10. Advantages and Disadvantages
### Advantages:
* **Intuitive and Interpretative:** Offers immediate visual insight into the core structural dynamics of an economy.
* **Policy Relevance:** Directly mirrors the mandates of major dual-mandate central banks (e.g., US Federal Reserve).
* **Anomaly Detection:** Quickly flags historical anomalies and data regimes where traditional theory fails.

### Disadvantages:
* **Over-Simplification:** Reduces complex multi-variable macroeconomic networks into a single bivariate axis.
* **Instability:** The relationship is notoriously unstable over long multi-decade windows.

## 11. Best Practices and Practical Considerations
* **Always Test for Structural Breaks:** Use structural break tests (e.g., Chow Test or Quandt-Andrews Breakpoint Test) before fitting a global model to the entire time horizon.
* **Use Breakeven Rates for Forward-Looking Analysis:** Market-based inflation expectations (like 10-year breakevens) react faster than backward-looking CPI metrics, making them highly effective for asset allocation EDA.
* **De-trend Where Necessary:** Consider decomposing the series into cyclical and trend components to isolate short-run Phillips dynamics from long-run structural shifts.

## 12. Typical Visualizations Associated with the Analysis
* **Bivariate Scatter with Trendlines:** Shows the absolute relationship using OLS or LOWESS smoothers.
* **Time-Series Dual-Axis Plots:** Displays both metrics over time to trace cyclical patterns.
* **Rolling Correlation Plots:** Tracks the temporal stability of the correlation coefficient.
* **Cross-Correlation Function (CCF) Charts:** Bar charts demonstrating correlation strengths across negative and positive lag boundaries.