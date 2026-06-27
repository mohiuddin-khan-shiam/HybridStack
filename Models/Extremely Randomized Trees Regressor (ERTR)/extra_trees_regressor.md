# Extremely Randomized Trees (Extra Trees) Regressor

## 1. Background and Context
The **Extremely Randomized Trees** (commonly referred to as **Extra Trees**) algorithm, introduced by Pierre Geurts, Damien Ernst, and Louis Wehenkel in 2006, is an ensemble learning method primarily utilized for classification and regression tasks. It is a variant of the classic Random Forest algorithm belonging to the family of parallel perturbe-and-combine tree bagging techniques.

While Random Forest optimizes splits by searching exhaustively for the best local cut-point among a random selection of features, Extra Trees takes randomization a step further. Instead of computing the mathematically optimal threshold for each candidate feature, Extra Trees draws split thresholds completely at random. This aggressive injecting of randomness yields highly decorrelated individual decision trees, driving down variance significantly while trading off a minor, manageable increase in bias. Additionally, it offers a stark reduction in computational training times compared to traditional Random Forests.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Double Layer Randomization
The design principle of Extra Trees is governed by two orthogonal random mechanisms:
1. **Feature Subspace Selection:** At each node during tree growth, a random subset of $m$ features is sampled from the total $p$ available dimensions without replacement.
2. **Random Cut-Point Allocation:** For each selected feature in the candidate subset, a split threshold is generated uniformly at random across the feature's localized empirical range, rather than optimizing the split via an exhaustive grid search.

### 2.2. Mathematical Optimization of Selection
Let $S$ represent the parent dataset reaching a node. For a selected continuous attribute $a$, let $x_a^{\max}$ and $x_a^{\min}$ represent the maximum and minimum values of this attribute within $S$. A split threshold $a_c$ is sampled uniformly:

$$a_c \sim \mathcal{U}\left(x_a^{\min}, x_a^{\max}\right)$$

The data partition splits into two child subsets: $S_L = \{\mathbf{x} \in S \mid x_a \le a_c\}$ and $S_R = \{\mathbf{x} \in S \mid x_a > a_c\}$. 
To choose the single feature to execute from the $m$ random options, the algorithm evaluates the standard variance reduction metric (for regression tasks):

$$\Delta \text{Var}(S, a) = \text{Var}(S) - \frac{|S_L|}{|S|} \text{Var}(S_L) - \frac{|S_R|}{|S|} \text{Var}(S_R)$$

Where the sample variance $\text{Var}(S)$ over target scalar elements $y \in S$ containing mean $\bar{y}_S$ is:

$$\text{Var}(S) = \frac{1}{|S|} \sum_{i \in S} (y_i - \bar{y}_S)^2$$

The randomized feature candidate that maximizes $\Delta \text{Var}(S, a)$ is definitively chosen to establish the structural partition.

### 2.3. Ensemble Prediction
Just as in classical bagging systems, individual extremely randomized trees are grown to their full structural limit without pruning. For an unseen query sample $\mathbf{x}$, the regression output is the arithmetic mean across all $B$ configured decision trees:

$$\hat{f}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} \hat{f}_b(\mathbf{x})$$

---

## 3. Algorithm Description

1. **Initialization:** Set parameters including the total forest size $B$ (`n_estimators`), maximum depth boundaries (`max_depth`), and candidate feature capacity per split $m$.
2. **Tree Growth Phase:** For each tree $b = 1$ to $B$:
    * If `bootstrap=False`, allocate the complete un-sampled training dataset $D$ directly to the root node. If `bootstrap=True`, draw a sample with replacement.
    * Recursively develop nodes down the tree structure:
        * Stop splitting if the node sample size falls below `min_samples_split`, depth exceeds constraints, or targets are homogeneous.
        * Draw $m$ unique features at random from total feature indices.
        * For each drawn feature, sample a split point $a_c$ uniformly within its observed range.
        * Measure the variance reduction $\Delta \text{Var}$ for all $m$ randomly constructed thresholds.
        * Retain the single candidate feature and threshold maximizing that reduction, and divide the data into left and right sub-nodes.
3. **Inference Execution:** Run unseen inference samples through the accumulated forest of independent, decorrelated trees, returning their unweighted average prediction.