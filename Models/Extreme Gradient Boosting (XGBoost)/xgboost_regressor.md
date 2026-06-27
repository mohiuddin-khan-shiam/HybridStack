# Extreme Gradient Boosting (XGBoost) Regressor

## 1. Background and Context
**Extreme Gradient Boosting (XGBoost)** is an optimized, highly scalable, and efficient implementation of the Gradient Boosted Decision Tree (GBDT) framework. Introduced by Tianqi Chen and Carlos Guestrin in 2016, XGBoost was engineered to push the limits of computing power for boosted tree algorithms, offering parallel tree construction, cache-aware access patterns, and out-of-core computing capabilities.

Like standard gradient boosting, XGBoost builds an ensemble of weak learners (typically regression trees) sequentially to minimize a given loss function. However, XGBoost distinguishes itself by using a regularized objective function, a unique split-finding algorithm, and second-order Taylor expansions to optimize performance and prevent overfitting.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Regularized Objective Function
For a dataset with $n$ instances and $d$ features $D = \{(\mathbf{x}_i, y_i)\}$, an ensemble tree model uses $K$ additive functions to predict the output:

$$\hat{y}_i = \sum_{k=1}^{K} f_k(\mathbf{x}_i), \quad f_k \in \mathcal{F}$$

where $\mathcal{F}$ is the space of regression trees. To optimize the model, XGBoost minimizes the following regularized objective function:

$$\mathcal{L}(\phi) = \sum_{i=1}^{n} l(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k)$$

where $l$ is a differentiable convex loss function measuring the difference between prediction $\hat{y}_i$ and target $y_i$. The term $\Omega$ penalizes the complexity of the trees to mitigate overfitting:

$$\Omega(f) = \gamma T + rac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$$

where $T$ represents the number of leaves in the tree, and $w_j$ represents the score/weight of leaf $j$. The hyperparameters $\gamma$ and $\lambda$ control the magnitude of regularization.

### 2.2. Second-Order Taylor Approximation
Gradient boosting builds trees sequentially. At iteration $t$, let $\hat{y}_i^{(t-1)}$ be the prediction of instance $i$. The objective is to find a function $f_t$ that minimizes:

$$\mathcal{L}^{(t)} = \sum_{i=1}^{n} l\left(y_i, \hat{y}_i^{(t-1)} + f_t(\mathbf{x}_i)ight) + \Omega(f_t)$$

Using a second-order Taylor expansion, the objective can be approximated as:

$$\mathcal{L}^{(t)} pprox \sum_{i=1}^{n} \left[ l(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(\mathbf{x}_i) + rac{1}{2} h_i f_t^2(\mathbf{x}_i) ight] + \Omega(f_t)$$

where $g_i$ and $h_i$ are the first and second-order gradient statistics of the loss function:

$$g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}_i^{(t-1)}) \quad 	ext{and} \quad h_i = \partial^2_{\hat{y}^{(t-1)}} l(y_i, \hat{y}_i^{(t-1)})$$

By removing the constant terms independent of $f_t$, the simplified objective at step $t$ becomes:

$$	ilde{\mathcal{L}}^{(t)} = \sum_{i=1}^{n} \left[ g_i f_t(\mathbf{x}_i) + rac{1}{2} h_i f_t^2(\mathbf{x}_i) ight] + \gamma T + rac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$$

### 2.3. Optimal Leaf Weights and Structural Score
Let $I_j = \{i \mid q(\mathbf{x}_i) = j\}$ be the instance set allocated to leaf $j$. We can rewrite the objective function by grouping the instances by leaf node:

$$	ilde{\mathcal{L}}^{(t)} = \sum_{j=1}^{T} \left[ \left( \sum_{i \in I_j} g_i ight) w_j + rac{1}{2} \left( \sum_{i \in I_j} h_i + \lambda ight) w_j^2 ight] + \gamma T$$

For a fixed tree structure $q(\mathbf{x})$, the optimal weight $w_j^*$ for leaf $j$ is computed by setting the derivative with respect to $w_j$ to zero:

$$w_j^* = -rac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}$$

Substituting $w_j^*$ back into the objective function yields the optimal structural score (or quality score) of the tree:

$$	ilde{\mathcal{L}}^{(t)}(q) = -rac{1}{2} \sum_{j=1}^{T} rac{\left( \sum_{i \in I_j} g_i ight)^2}{\sum_{i \in I_j} h_i + \lambda} + \gamma T$$

### 2.4. Gain-Based Node Splitting
When constructing a tree, it is computationally prohibitive to evaluate all possible tree configurations. Instead, a greedy algorithm starts from a single root node and iteratively adds splits. The score gain of splitting a leaf into left ($L$) and right ($R$) sub-nodes is defined as:

$$	ext{Gain} = rac{1}{2} \left[ rac{\left( \sum_{i \in I_L} g_i ight)^2}{\sum_{i \in I_L} h_i + \lambda} + rac{\left( \sum_{i \in I_R} g_i ight)^2}{\sum_{i \in I_R} h_i + \lambda} - rac{\left( \sum_{i \in I} g_i ight)^2}{\sum_{i \in I} h_i + \lambda} ight] - \gamma$$

This equation evaluates the quality improvement brought by a split. If the calculated $	ext{Gain}$ is less than $\gamma$, the split is discarded.

---

## 3. Algorithm Description

1. **Initialization:** Initialize the model with a base constant prediction (typically $\hat{y}_i^{(0)} = 0.5$ or the mean of the labels).
2. **Sequential Boosting Iterations:** For $t = 1, 2, \dots, K$:
    * Compute the first-order gradients $g_i$ and second-order gradients $h_i$ for all instances in the dataset based on the current ensemble predictions $\hat{y}_i^{(t-1)}$.
    * Build a new regression tree structure $f_t$:
        * Start at the root node containing all instances.
        * For each leaf node, evaluate all available features and possible split points using the $	ext{Gain}$ formula.
        * Apply feature and instance subsampling strategies (colsample_bytree, subsample) if configured.
        * Split nodes greedily until the maximum depth (`max_depth`) is reached or no further splits yield a positive gain.
    * Compute the optimal leaf scores $w_j^*$ for all leaves in the new tree.
    * Update the ensemble predictions by adding the scaled tree contributions:
      $$\hat{y}_i^{(t)} = \hat{y}_i^{(t-1)} + \eta \cdot f_t(\mathbf{x}_i)$$
      where $\eta$ is the learning rate (`learning_rate`).
3. **Termination:** Stop when the total number of boosting rounds ($K$) is completed or early stopping criteria are triggered.
