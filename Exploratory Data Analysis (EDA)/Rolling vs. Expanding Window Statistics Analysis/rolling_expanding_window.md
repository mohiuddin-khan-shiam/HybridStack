# Rolling vs. Expanding Window Statistics Analysis (Temporal Window Filtering EDA)

## 1. Introduction and Purpose
**Rolling vs. Expanding Window Statistics Analysis** is a fundamental exploratory data analysis (EDA) technique for time-series and sequential data. Its primary purpose is to capture structural trajectories, trace baseline evolution, and evaluate chronological stability by computing statistics over localized sliding or growing windows. While **Rolling Windows** track localized, moving changes over a fixed temporal horizon (capturing recent momentum and regime shifts), **Expanding Windows** compile a continuous cumulative baseline incorporating *all* historical data up to that point. In data science, engineering, and predictive pipelines, this comparison separates short-term cyclical variance from long-term structural trends and tests for structural breaks.

## 2. Background and Motivation
Raw sequential data frequently contains high-frequency noise, transient shocks, and strong seasonal spikes that obscure structural movements. Analyzing data using a dual window strategy is critical because:
* **Separating Frequencies:** It isolates high-frequency fluctuations (raw data), medium-frequency movements (rolling metrics), and low-frequency baseline drifts (expanding metrics).
* **Quantifying Accumulation:** It highlights cumulative paths or "memory accumulation" profiles (such as total historical mean adjustments) which are crucial for stable baseline modeling.
* **Detecting structural drift:** If a rolling metric drifts significantly away from its long-term expanding counterpart, it signals a non-stationary process or an active structural break.

## 3. Theoretical Foundation
The theoretical core of temporal window statistics relies on the concepts of **ergodicity**, **stationarity**, and **low-pass filtration**. 

* **Rolling Window Filters:** Operate as an elastic, fixed-size window $W$ that discards historical data older than $t-W$. This behaves like a low-pass filter, smoothing out high-frequency noise while preserving short-term momentum and localized regime shifts.
* **Expanding Window Filters:** Increase their window size at every step, meaning the horizon grows dynamically to encompass the entire historical timeline ($[1, t]$). As $t 	o \infty$, the expanding metric converges toward the true global population statistic if the system is stationary, making it an excellent benchmark for stability.

## 4. Statistical Concepts and Mathematical Equations
Let $X = \{X_1, X_2, \dots, X_t\}$ represent a chronologically ordered sequence of numerical observations up to time step $t$.

### A. Rolling Window Statistics (Fixed Window $W$)
At time index $t$ (where $t \ge W$), the subset of observations falls within the interval $\{X_{t-W+1}, \dots, X_t\}$. The standard Rolling Mean ($\mu_{	ext{roll}, t}$) and Rolling Variance ($\sigma^2_{	ext{roll}, t}$) are defined as:
$$\mu_{	ext{roll}, t} = rac{1}{W} \sum_{i=0}^{W-1} X_{t-i}$$
$$\sigma^2_{	ext{roll}, t} = rac{1}{W-1} \sum_{i=0}^{W-1} (X_{t-i} - \mu_{	ext{roll}, t})^2$$

### B. Expanding Window Statistics (Growing Window)
At time index $t$, the calculation includes all data points from the initial starting step $1$ up to the current step $t$. The Expanding Mean ($\mu_{	ext{exp}, t}$) and Expanding Variance ($\sigma^2_{	ext{exp}, t}$) are defined as:
$$\mu_{	ext{exp}, t} = rac{1}{t} \sum_{i=1}^{t} X_i$$
$$\sigma^2_{	ext{exp}, t} = rac{1}{t-1} \sum_{i=1}^{t} (X_i - \mu_{	ext{exp}, t})^2$$

## 5. Methodology or Workflow
The systematic execution of a Rolling vs. Expanding Statistics EDA follows these sequential steps:
1. **Chronological Alignment:** Verify that the sequence features a strictly ordered index with uniform time step intervals.
2. **Lookback Window Selection:** Choose an analytically sound fixed window size ($W$) for the rolling operations based on the data's natural cycles (e.g., $W=30$ for daily tracking over a typical month).
3. **Rolling Calculation Pipeline:** Compute the localized statistical summary metrics (means, standard deviations, quantiles) across the moving windows.
4. **Expanding Calculation Pipeline:** Compute the cumulative statistical metrics across the growing historical horizon.
5. **Stability Gap Profiling:** Calculate the difference between the rolling and expanding metrics ($\mu_{	ext{roll}} - \mu_{	ext{exp}}$) to identify structural shifts or regime changes.
6. **Diagnostic Visualization Grid:** Generate unified multi-panel charts overlaying the raw series with both window tracks to evaluate smoothing lags and stability.

## 6. Input Data Requirements
* **Temporal Ordering:** Monotonically increasing time stamps or sequential integer indices.
* **Data Completeness:** Continuous numerical values. Missing intervals or NaN spaces should be handled using interpolation or forward fills before running window operations.
* **Sample Horizon Bounds:** The total length of the sequence $N$ must be larger than the chosen rolling window width ($N > W$) to allow for meaningful window movement over time.

## 7. Expected Outputs and Interpretations
* **Dual Trend Overlay Plot:** Overlays the raw data with the rolling and expanding lines.
  * The **Rolling line** tracks the data more closely, showing short-term cyclical patterns and localized changes in direction.
  * The **Expanding line** is much smoother and less sensitive to short-term changes, stabilizing over time to reveal the true long-term baseline direction.
* **Phase Lag Observations:** The rolling line will naturally show a slight time lag behind major sudden shifts in the raw data, with the size of the lag proportional to the window width ($pprox rac{W-1}{2}$).
* **Convergence Behavior:** In a stable, stationary system, the expanding line will gradually flatten out and settle around a single constant value as it absorbs more history. If the expanding line continues to climb or fall steadily without flattening, it confirms that the underlying process has a long-term structural trend.

## 8. Assumptions and Limitations
* **Lookback Lag Trade-off:** Choosing a rolling window involves a distinct trade-off: a small window removes less noise but reacts quickly to real changes, while a large window produces a smoother line but introduces a significant time delay (phase lag).
* **Startup Gaps:** The first $W-1$ data points in a rolling analysis will be empty (NaN) because there isn't enough history to fill the initial window size.
* **Outlier Sensitivity:** A single massive, short-term data spike will create a temporary "step" or plateau in a rolling window that lasts for exactly $W$ periods. In an expanding window, that same spike will permanently alter the baseline calculation, though its impact will slowly fade as more data is added.

## 9. Common Use Cases
* **Macroeconomic Baseline Estimation:** Monitoring long-term consumer price indexes or GDP growth configurations by separating holiday noise from multi-decade expanding averages.
* **Financial Signal Engineering:** Building trailing indicators (such as rolling and expanding Z-scores or momentum thresholds) to serve as features in machine learning and algorithmic trading strategies.
* **Operational Capacity Planning:** Tracking server load metrics or customer traffic streams to compare immediate weekly variations against long-term operational infrastructure baselines.

## 10. Advantages and Disadvantages
### Advantages:
* **Multi-Scale Context:** Evaluates short-term changes (rolling window) and long-term historical context (expanding window) at the same time within a single visual framework.
* **Simple and Transparent:** Computationally efficient and highly interpretable for both technical teams and business stakeholders.
* **Dynamic Baselining:** Automatically adjusts to tracking values over time without requiring complex assumptions about the data's underlying statistical distribution.

### Disadvantages:
* **Inherent Response Lag:** Delays the identification of key structural turning points because the metrics are backward-looking.
* **Arbitrary Window Bias:** The insights gained from the rolling analysis depend heavily on your chosen window size parameter ($W$).

## 11. Best Practices and Practical Considerations
* **Align Windows with Inherent Cycles:** Match your rolling window size to known operational or seasonal periods (e.g., use 7 for daily data with weekly habits, or 12 for monthly data with annual patterns).
* **Combine Means with Volatility Bands:** Don't just track the window averages; plot rolling standard deviations alongside them to see how the data's volatility changes over time.
* **Use Minimum Periods to Avoid Gaps:** Use settings like `min_periods=1` in your calculations if you need to generate baseline metrics for the early startup phase of your dataset rather than leaving those rows blank.

## 12. Typical Visualizations Associated with the Analysis
* **Unified Dual-Window Overlay Plot:** A time-series chart showing the raw sequence overlaid with both the moving rolling lines and the cumulative expanding lines.
* **Residual Tracking Subplot:** A secondary plot tracking the difference between the rolling and expanding metrics to quickly highlight moments of structural change or economic regime shifts.