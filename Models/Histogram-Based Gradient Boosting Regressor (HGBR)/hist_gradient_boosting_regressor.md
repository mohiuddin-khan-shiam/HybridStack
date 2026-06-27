# Histogram-Based Gradient Boosting Regressor (HGBR)

## 1. Background and Context
The **Histogram-Based Gradient Boosting Regressor (HGBR)** is an advanced, highly optimized variant of the Gradient Boosted Decision Tree (GBDT) framework. It is heavily inspired by LightGBM and was introduced to Scikit-Learn to overcome the critical scalability limits of traditional GBDT implementations on large-scale datasets.

In standard gradient boosting, finding the optimal split point for a continuous feature requires sorting the feature values for all instances at every node. This sorting operation has a computational complexity of $O(n \log n)$ per feature, which becomes prohibitively slow as the number of samples $n$ scales into hundreds of thousands or millions. HGBR addresses this by discretizing (binning) continuous features into integer-valued bins (typically $\le 255$). By converting the data into a histogram representation, the split-finding complexity drops to $O(n)$ during the initial binning stage and $O(\text{max\_bins})$ at each tree node, radically speeding up training times and lowering memory consumption.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Feature Discretization (Binning)
Before any decision trees are constructed, each continuous input feature $x_j$ is mapped to a discrete integer bin index $\tilde{x}_j \in \{0, 1, \dots, K-1\}$, where $K$ is the maximum number of bins (`max_bins`, default up to 255). 

The bin boundaries are computed automatically based on the quantiles of the feature distribution. For a feature value $x_{ij}$, the transformation is defined as:

$$\tilde{x}_{ij} = k \quad \text{if} \quad b_{k} \le x_{ij} < b_{k+1}$$

where $b_k$ and $b_{k+1}$ are the learned lower and upper quantitative thresholds for bin $k$. An extra bin index is reserved exclusively to handle missing values natively, preventing the need for manual imputation.

### 2.2. Gradient and Hessian Histograms
During sequential boosting rounds, the algorithm calculates the first-order gradient $g_i$ and constant second-order gradient (Hessian) $h_i$ of the objective loss function for each sample $i$:

$$g_i = \left[ \frac{\partial L(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)} \right]_{F(\mathbf{x}) = F_{m-1}(\mathbf{x})}, \quad h_i = \left[ \frac{\partial^2 L(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)^2} \right]_{F(\mathbf{x}) = F_{m-1}(\mathbf{x})}$$

For standard squared error (regression tasks), $L(y, \hat{y}) = \frac{1}{2}(y - \hat{y})^2$, meaning $g_i = \hat{y}_i - y_i$ and $h_i = 1$.

Instead of iterating through raw samples to compute potential splits, HGBR aggregates these statistics into histograms for each bin $k$ of feature $j$:

$$G_j(k) = \sum_{i: \tilde{x}_{ij} = k} g_i, \quad H_j(k) = \sum_{i: \tilde{x}_{ij} = k} h_i$$

### 2.3. Optimal Split-Finding and Gain Optimization
When deciding where to split a node, the algorithm evaluates partitions between discrete bins. The split-finding routine scans the aggregated bins from $1$ to $K-1$. The optimization gain for splitting at bin threshold $k$ is calculated as:

$$\text{Gain} = \frac{1}{2} \left[ \frac{\left( \sum_{k \le k_{\text{split}}} G_j(k) \right)^2}{\sum_{k \le k_{\text{split}}} H_j(k) + \lambda} + \frac{\left( \sum_{k > k_{\text{split}}} G_j(k) \right)^2}{\sum_{k > k_{\text{split}}} H_j(k) + \lambda} - \frac{\left( \sum_{k} G_j(k) \right)^2}{\sum_{k} H_j(k) + \lambda} \right]$$

where $\lambda$ represents the L2 regularization factor on leaf weights. The split maximizing this gain expression is chosen.

### 2.4. Subtraction Trick for Accelerated Tree Building
To build histogram structures even faster, HGBR uses the **histogram subtraction trick**. When a parent node splits into a left child and a right child, the histogram of the parent node is already calculated. The algorithm only computes the histogram for the smaller child node directly from its samples ($O(n_{\text{small}})$). The histogram of the larger child node is computed by subtracting the smaller child's histogram from the parent's histogram:

$$\text{Histogram}(\text{Child}_{\text{large}}) = \text{Histogram}(\text{Parent}) - \text{Histogram}(\text{Child}_{\text{small}})$$

This operation takes only $O(K)$ instructions, which is independent of the number of samples in that node.

---

## 3. Algorithm Description

1. **Pre-processing and Global Binning:**
    * Quantize all continuous features into discrete, integer-valued histograms of size `max_bins`.
2. **Sequential Tree Construction Iterations:** For $m = 1, 2, \dots, M$ (where $M$ corresponds to `max_iter`):
    * Calculate the operational gradient vector $g$ and Hessian vector $h$ across the training population.
    * Construct a new regression tree using the discrete bin values:
        * Aggregate gradients and Hessians into feature histograms at the root node.
        * Evaluate optimal split thresholds between bins using the structural gain formula.
        * Apply the histogram subtraction trick to compute the histograms of downstream child nodes instantly.
        * Continue splitting leaves vertically until structural limits (`max_depth` or `min_samples_leaf`) are reached.
    * Calculate the optimal output value for each leaf node based on the final subset of samples it contains.
    * Add the newly grown tree's predictions to the ensemble model, scaled by the learning rate parameter ($\nu$):
      $$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \nu \cdot h_m(\mathbf{x})$$
3. **Inference Execution:** Map the raw features of an unseen instance to their corresponding bin structures, route them through the ensemble of trees, and return the aggregated prediction sum.