# Time Shifting and Lead-Lag Analysis (Temporal Phase Shift EDA)

## 1. Introduction and Purpose
**Time Shifting and Lead-Lag Analysis** is a fundamental exploratory data analysis (EDA) technique in time-series processing used to realign or displace sequential observations along the chronological timeline. Its primary purpose is to manually construct **Lags** (shifting historical observations forward into future index positions) and **Leads** (shifting future observations backward into past index positions). In data science, econometrics, and predictive modeling, time shifting serves as the structural foundation for feature engineering, letting analysts evaluate immediate momentum, map historical dependencies, expose phase mismatches, and prepare supervised training matrices for autoregressive algorithms.

## 2. Background and Motivation
In time-series analytics, observations are bound together by their chronological order. Raw snapshots can mask the true relationship between variables because causes do not always yield immediate, real-time effects. Analyzing temporal displacements via time shifting addresses several exploratory bottlenecks:
* **Autoregressive Feature Engineering:** To forecast the future state of a variable, models require direct access to its recent historical properties (e.g., predicting $Y_t$ using $Y_{t-1}$ and $Y_{t-2}$).
* **Lead-Lag Validation:** It reveals whether a sequence physically precedes or trails another, such as checking if changes in wholesale commodity pricing lead changes in consumer inflation indexes.
* **Supervised Training Transformation:** It transforms a single sequential vector into a multi-column supervised learning matrix containing both inputs (historical lags) and targets (future leads).

## 3. Theoretical Foundation
The theoretical core of time shifting relies on **temporal displacement operators** and **phase-space alignments**. Traditional cross-sectional algorithms treat data rows as independent samples. In contrast, time-series analysis evaluates data as a stochastic process where past states influence current and future outcomes.

Displacing a sequence creates a localized phase shift across the dataset. Shifting data forward aligns old observations with new timestamps, making it easy to measure serial correlation (autocorrelation) and track momentum variations.

## 4. Statistical Concepts and Mathematical Equations
Let a raw time-series sequence be represented by a set of values $\mathbf{Y} = \{y_1, y_2, \dots, y_N\}$ indexed by a monotonic time sequence $t = 1, 2, \dots, N$.

### A. The Backward Shift Operator (Lag Operator)
The lag operator $L$ (or $B$) shifts an observation backward in time by $k$ periods, aligning historical data with the current time step $t$:
$$L^k y_t = y_{t-k}$$
For example, a lag of 1 ($k=1$) matches yesterday's value with today's timestamp:
$$L^1 y_t = y_{t-1}$$

### B. The Forward Shift Operator (Lead Operator)
The lead operator $F$ (or $L^{-1}$) shifts an observation forward in time by $k$ periods, aligning future data with the current time step $t$:
$$F^k y_t = y_{t+k}$$
For example, a lead of 1 ($k=1$) matches tomorrow's value with today's timestamp:
$$F^1 y_t = y_{t+1}$$

### C. Boundary Missingness and Null Generation
Because shifting displaces the data points relative to the fixed time index, it introduces empty cells at the boundaries of the dataset:
* Applying a lag of $k$ leaves the first $k$ rows empty: $\{y_1, \dots, y_k\} 	o 	ext{NaN}$
* Applying a lead of $k$ leaves the last $k$ rows empty: $\{y_{N-k+1}, \dots, y_N\} 	o 	ext{NaN}$

## 5. Methodology or Workflow
The systematic execution of a Time Shifting and Lead-Lag Analysis EDA follows these sequential steps:
1. **Index Monotonicity Check:** Validate that the input sequence is explicitly sorted in increasing chronological order with uniform time steps.
2. **Lag Parameter Definition:** Select the appropriate step size $k$ for the displacement based on the data's frequency and natural business cycles (e.g., $k=1$ for immediate momentum, or $k=12$ for annual cycles in monthly datasets).
3. **Lag Generation Pipeline:** Displace the target series forward by $k$ steps to align past observations with current timestamps, creating lookback features.
4. **Lead Generation Pipeline:** Displace the target series backward by $k$ steps to align future observations with current timestamps, creating lookahead targets.
5. **Boundary Truncation:** Remove or mask the empty rows (NaN cells) generated at the boundaries to ensure clean data matrices for subsequent modeling steps.
6. **Phase Overlays Visualization:** Plot the original data overlaid with the shifted tracks to visually inspect the lookback lags, phase delays, and lookahead targets.

## 6. Input Data Requirements
* **Temporal Ordering:** A validated pandas `DatetimeIndex` or a strictly monotonic integer sequence.
* **Continuous Intervals:** Best applied to time series with uniform frequencies (e.g., daily, monthly, quarterly).
* **Numerical Typology:** Standard continuous numerical sequences.

## 7. Expected Outputs and Interpretations
* **Shifted Feature Dataframe:** An expanded table containing the original series alongside the newly generated lag columns ($Y_{t-k}$) and lead columns ($Y_{t+k}$).
* **Phase Alignment Plot:** A time-series chart showing the original and shifted lines.
  * The **Lagged line** mirrors the original curve but appears shifted to the right, highlighting the lookback history and phase delay.
  * The **Lead line** mirrors the original curve but appears shifted to the left, showing the future lookahead trajectory.
* **Truncated Rows:** Visualizing how the boundary rows turn into empty cells (NaN) helps analysts plan the proper trimming steps needed to avoid training errors or data leakage.

## 8. Assumptions and Limitations
* **Introduces Boundary Gaps:** Every shift operation removes usable data points from the edges of your dataset ($k$ empty cells per shift), which can significantly reduce your sample size when working with small datasets or large lag sizes.
* **Assumes Uniform Spacing:** The shift operator moves data by a fixed number of rows, not by a specific duration of time. If your dataset has missing dates or irregular intervals, shifting rows will mismatch the time steps unless you reindex the data first.
* **Risk of Data Leakage:** Using lead features ($Y_{t+k}$) as inputs in a predictive model introduces **lookahead bias** by feeding future information into past steps, which can ruin the validity of your backtests. Leads should only be used as target variables.

## 9. Common Use Cases
* **Supervised Learning Feature Prep:** Converting raw sequential data into an automated feature matrix with multiple lag columns to train models like Random Forests, XGBoost, or linear regressions.
* **Target Label Construction:** Generating lookahead target columns (leads) to set up multi-step-ahead forecasting models.
* **Momentum Feature Engineering:** Creating difference metrics (e.g., $Y_t - Y_{t-1}$) to track immediate growth or decline rates.

## 10. Advantages and Disadvantages
### Advantages:
* **Enables Standard Supervised Learning:** Converts a single time-series vector into a multi-column feature space, letting you use standard cross-sectional machine learning algorithms.
* **Simple and Transparent:** Computationally efficient, requiring simple index adjustments without complex mathematical transformations.
* **Flexible Lag Configurations:** Supports custom lookback and lookahead structures tailored to various seasonalities and frequencies.

### Disadvantages:
* **Reduces Sample Size:** Shortens the usable dataset by creating empty rows at the boundaries.
* **Prone to Data Leakage:** High risk of accidentally introducing future information into models if lead variables are misconfigured as input features.

## 11. Best Practices and Practical Considerations
* **Reindex Before Shifting:** If your dataset contains irregular intervals or missing dates, always resample or reindex the timeline to a uniform frequency before shifting rows to ensure accurate time displacements.
* **Never Use Leads as Model Inputs:** Keep a strict separation between lookback variables (lags) and lookahead targets (leads) to prevent data leakage and lookahead bias.
* **Drop Null Rows Securely:** Use operations like `.dropna()` on your final feature dataframe to cleanly remove the empty boundary rows before passing the data into machine learning algorithms.

## 12. Typical Visualizations Associated with the Analysis
* **Temporal Phase Overlay Plot:** A time-series line plot overlaying the original data with its lagged and lead variants to verify phase shifts and alignment accuracy.
* **Boundary Missingness Matrix:** A visual grid highlighting the empty cells (NaN) at the edges of the dataset to show the structural data loss caused by shifting.