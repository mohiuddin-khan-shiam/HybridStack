# Comprehensive Evaluation Metrics Reference Manual: Regression

This manual serves as a definitive, mathematical, and practical reference guide for regression, time-series forecasting, and continuous value estimation model evaluation metrics. It defines standard error measurements, scale-independent formulations, and goodness-of-fit benchmarks.

---

## 1. Overview and Metric Selection Framework

Selecting the optimal evaluation metric requires analyzing the underlying data distribution, the business impact of small vs. large errors, and the scale characteristics of the dependent variable. 

### Metric Comparison Matrix

| Full Name & Abbreviation | Optimization Objective | Scale Dependence | Sensitivity to Outliers | Handles Zero Values | Typical Applications |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mean Squared Error (MSE)** | Lower is better ($\\rightarrow 0$) | Dependent | High (Quadratic penalty) | Yes | Deep Learning loss, Physics modeling |
| **Root Mean Squared Error (RMSE)** | Lower is better ($\\rightarrow 0$) | Dependent | High (Quadratic penalty) | Yes | Operational tracking, Engineering |
| **Mean Absolute Error (MAE)** | Lower is better ($\\rightarrow 0$) | Dependent | Linear (Robust) | Yes | Financial forecasting, Supply chain |
| **Mean Absolute Percentage Error (MAPE)** | Lower is better ($\\rightarrow 0$) | Scale-Independent | Asymmetric / Sensitive near zero | No (Requires adjustment / epsilon) | Business reporting, Sales forecasting |
| **Symmetric Mean Absolute Percentage Error (sMAPE)** | Lower is better ($\\rightarrow 0$) | Scale-Independent | Symmetrical bound ($[0, 200\%]$) | Yes (If $y_t, \\hat{y}_t$ aren't both 0) | Demand planning, Inventory management |
| **Mean Absolute Scaled Error (MASE)** | Lower is better ($< 1$ beats naive) | Scale-Independent | Linear (Relative to naive baseline) | Yes | Time-series forecasting, Econometrics |
| **Coefficient of Determination ($R^2$)** | Higher is better ($\\rightarrow 1$) | Scale-Independent | High (Based on squared residuals) | Yes | Statistical validation, Explanatory models |

---

## 2. In-Depth Metric Analysis

### 2.1 Mean Squared Error (MSE)
* **Full Name:** Mean Squared Error (MSE)
* **Introduction & Purpose:** Measures the average squared difference between true outcomes and predictions. It serves as the primary optimization objective function (loss function) for a majority of linear, tree-based, and deep learning estimators.
* **Background & Motivation:** Derived from Gaussian maximum likelihood estimation frameworks, minimizing MSE corresponds directly to finding the conditional mean of the target distribution.
* **Mathematical Definition:**
  $$\\text{MSE} = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2$$
* **Step-by-step Calculation:**
  1. Calculate the difference $(y_i - \\hat{y}_i)$ for each sample.
  2. Square each individual difference to eliminate negative signs and amplify large errors.
  3. Sum all squared values and divide by the sample size $n$.
* **Interpretation:** Measures variance plus the squared bias of predictions. Units are squared units of the target value (e.g., if target is dollars, MSE is in $\\text{dollars}^2$), making raw values difficult to interpret intuitively.
* **Value Range:** $[0, +\\infty)$. A value of $0$ indicates perfect predictions.
* **Advantages:** Mathematically convenient, continuously differentiable (enabling gradient descent optimization), and highly responsive to catastrophic outliers.
* **Disadvantages:** Severely distorted by a few extreme outliers; non-intuitive units.
* **Assumptions & Limitations:** Assumes that large errors are exponentially more damaging than small errors.
* **Appropriate Use Cases:** High-stakes engineering or clinical frameworks where missing a critical threshold by a large margin results in catastrophic system failure.
* **Comparison with Others:** More sensitive to outliers than MAE; less interpretable than RMSE.

### 2.2 Root Mean Squared Error (RMSE)
* **Full Name:** Root Mean Squared Error (RMSE)
* **Introduction & Purpose:** Provides an outlier-sensitive error scale directly comparable to the target variable's native unit.
* **Mathematical Definition:**
  $$\\text{RMSE} = \\sqrt{\\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2}$$
* **Step-by-step Calculation:** Calculate the Mean Squared Error (MSE), then extract its square root.
* **Interpretation:** Reflects the typical standard deviation of the residuals.
* **Value Range:** $[0, +\\infty)$, where $0$ represents a perfect fit.
* **Advantages:** Preserves the outlier-penalizing characteristics of MSE while restoring physical or monetary interpretability.
* **Disadvantages:** Like MSE, a small subset of heavily mispredicted points can drastically inflate the final metric, masking otherwise excellent overall model performance.
* **Appropriate Use Cases:** Real estate valuation, stock pricing, and climate metrics where deviations are penalized quadratically but reportability matters.

### 2.3 Mean Absolute Error (MAE)
* **Full Name:** Mean Absolute Error (MAE)
* **Introduction & Purpose:** Measures the average absolute distance between predictions and actual values. It offers a clear picture of expected nominal error.
* **Background & Motivation:** Minimizing MAE corresponds to estimating the conditional median of the target variable, making it naturally resilient to long-tailed distributions.
* **Mathematical Definition:**
  $$\\text{MAE} = \\frac{1}{n} \\sum_{i=1}^{n} |y_i - \\hat{y}_i|$$
* **Interpretation:** Represents the expected absolute deviation per observation. If MAE is 5.0, the model is off by an average magnitude of 5.0 units.
* **Value Range:** $[0, +\\infty)$.
* **Advantages:** Intuitive interpretation, robust to extreme outliers, and treats all errors linearly.
* **Disadvantages:** The absolute value function contains a non-differentiable point at zero ($y_i = \\hat{y}_i$), which complicates direct gradient optimization without smoothing approximations.
* **Appropriate Use Cases:** Daily supply chain demand, manufacturing tolerances, or financial portfolios where an error of 20 units is exactly twice as costly as an error of 10 units.

### 2.4 Mean Absolute Percentage Error (MAPE)
* **Full Name:** Mean Absolute Percentage Error (MAPE)
* **Introduction & Purpose:** Translates errors into percentage terms, allowing analysts to compare model predictive accuracy across completely different scales.
* **Mathematical Definition:**
  $$\\text{MAPE} = \\frac{100\\%}{n} \\sum_{i=1}^{n} \\left| \\frac{y_i - \\hat{y}_i}{y_i} \\right|$$
* **Interpretation:** Expresses the average error magnitude as a percentage of the actual values.
* **Value Range:** $[0, +\\infty)$.
* **Advantages:** Intuitive for senior business leadership; independent of data scale.
* **Disadvantages:** Heavily asymmetric. If the actual value $y_i$ is tiny, any absolute error causes an enormous percentage spike. Conversely, if $y_i$ is huge, large absolute errors appear trivial.
* **Assumptions & Limitations:** Strictly invalid if any actual value $y_i = 0$, leading to division-by-zero.
* **Appropriate Use Cases:** Macroscopic sales projections, regional revenue forecasting, and metrics where comparative relative performance across departments is needed.

### 2.5 Symmetric Mean Absolute Percentage Error (sMAPE)
* **Full Name:** Symmetric Mean Absolute Percentage Error (sMAPE)
* **Introduction & Purpose:** Designed as an alternative to MAPE to bound percentage errors and treat under-forecasting and over-forecasting more symmetrically.
* **Mathematical Definition:**
  $$\\text{sMAPE} = \\frac{200\\%}{n} \\sum_{i=1}^{n} \\frac{|y_i - \\hat{y}_i|}{|y_i| + |\\hat{y}_i|}$$
* **Interpretation:** Provides a bounded percentage error metric centered around the average of true and predicted values.
* **Value Range:** $[0\\%, 200\\%]$.
* **Advantages:** Bounded maximum error prevents single low-value samples from driving the entire summary metric to infinity.
* **Disadvantages:** Still exhibits structural instabilities when both $y_i$ and $\\hat{y}_i$ approach zero. Can lead to non-intuitive evaluations because the denominator changes with the prediction itself.

### 2.6 Mean Absolute Scaled Error (MASE)
* **Full Name:** Mean Absolute Scaled Error (MASE)
* **Introduction & Purpose:** Compares the performance of a regression/forecasting model to an in-sample, baseline non-seasonal or seasonal naive forecast. It is a fundamental benchmark for time-series modeling.
* **Background & Motivation:** Proposed by Hyndman and Koehler (2006) to overcome the division-by-zero flaws of MAPE and the scale dependencies of MAE.
* **Mathematical Definition:**
  $$\\text{MASE} = \\frac{\\text{MAE}}{\\frac{1}{N-m}\\sum_{t=m+1}^{N}|y_t - y_{t-m}|}$$
  *Where $m$ is the seasonal periodicity ($m=1$ for non-seasonal).*
* **Interpretation:** * $\\text{MASE} < 1.0$: The model out-performs the naive baseline forecast.
  * $\\text{MASE} > 1.0$: The model performs worse than a simple persistence/naive strategy.
* **Value Range:** $[0, +\\infty)$.
* **Advantages:** Uniformly defined across zero-valued series, scale-independent, symmetric, and provides an immediate benchmark against trivial baselines.
* **Appropriate Use Cases:** Intermittent demand forecasting, structural financial time-series, macro-economic metrics, and comparing multi-step ahead forecasts across disparate entities.

### 2.7 Coefficient of Determination ($R^2$)
* **Full Name:** Coefficient of Determination ($R^2$ Score)
* **Introduction & Purpose:** Measures the proportion of the target variable's variance that is explained by the model features.
* **Mathematical Definition:**
  $$R^2 = 1 - \\frac{\\text{SS}_{\\text{res}}}{\\text{SS}_{\\text{tot}}} = 1 - \\frac{\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2}{\\sum_{i=1}^{n}(y_i - \\bar{y})^2}$$
* **Interpretation:** Indicates model explanatory power compared to a horizontal line drawn at the sample mean $\\bar{y}$.
* **Value Range:** $(-\\infty, 1.0]$. An $R^2 = 1.0$ represents a perfect fit. An $R^2 = 0.0$ indicates performance identical to predicting the mean. Negative values indicate the model performs worse than simply predicting the mean.
* **Disadvantages:** Inflated by adding independent variables regardless of their true predictive power (can be addressed using Adjusted $R^2$). It does not indicate model bias.
* **Appropriate Use Cases:** Statistical exploration, econometrics, social science regressions, and baseline goodness-of-fit assessments.

---

## 3. Metric Selection Framework & Guidelines

1. **If your data contains major outliers and they are valid anomalies that you must capture accurately:** Use **MSE** or **RMSE**.
2. **If your data contains major outliers but they are caused by measurement noise or sensor errors that you want to ignore:** Use **MAE**.
3. **If you are evaluating models across multiple product categories with vastly different absolute volume scales (e.g., small stores vs. megastores):** Use **MASE** or **sMAPE** (avoid MAPE if zero sales occur).
4. **If you need an explanatory metric for a business presentation or corporate dashboard to explain variance coverage:** Use **$R^2$ Score**.

---

## 4. Common Pitfalls and Best Practices

* **The Zero-Variance Trap:** Calculating $R^2$ on a dataset where all true target values are identical (e.g., in highly filtered subsets) results in a division-by-zero ($\\text{SS}_{\\text{tot}} = 0$). Always validate target variance before computing $R^2$.
* **Mismatched Dimensionality:** Passing a 2D column vector `(N, 1)` and a 1D row array `(N,)` into error computations can cause NumPy to broadcast the operation into an `(N, N)` matrix instead of calculating an element-wise difference. Always flatten or reshape inputs explicitly using safe wrappers like `np.asarray(y).ravel()`.
* **Relying Only on $R^2$ for Non-linear Models:** $R^2$ can be highly misleading or structurally non-applicable for complex non-linear models or out-of-sample data validations. Always complement $R^2$ with raw scale-dependent error metrics like RMSE or MAE.
