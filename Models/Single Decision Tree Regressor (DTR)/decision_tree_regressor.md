# Decision Tree Regressor

## 1. Background and Context
The **Decision Tree Regressor** is a fundamental non-parametric supervised learning algorithm used for regression tasks. Developed in its modern form under the Classification and Regression Trees (CART) framework by Leo Breiman, Jerome Friedman, Richard Olshen, and Charles Stone in 1984, it models relationships by recursively partitioning the feature space into distinct, non-overlapping regions.

Unlike linear regression frameworks that assume a global mathematical relationship between inputs and outputs, decision trees map complex non-linear interactions by constructing a hierarchical tree structure. The model isolates localized data segments, making it highly flexible, intuitive to interpret, and robust to outliers. It also requires minimal data preprocessing, such as scaling or normalization. However, unconstrained decision trees are highly prone to variance and overfitting, which is typically managed through hyperparameter constraints or ensemble pruning.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Feature Space Partitioning
A regression tree maps a predictive function by dividing a $p$-dimensional feature space into $M$ disjoint regions $R_1, R_2, \dots, R_M$. For any incoming instance vector $\mathbf{x}$ falling into region $R_m$, the model predicts a constant value $c_m$, which is mathematically derived as the sample mean of the target values $y_i$ within that region:

$$c_m = \frac{1}{N_m} \sum_{\mathbf{x}_i \in R_m} y_i$$

where $N_m$ is the total number of training instances allocated to region $R_m$.

### 2.2. Recursive Binary Splitting optimization
The CART framework employs a greedy, top-down approach known as **Recursive Binary Splitting**. Starting at the root node, the algorithm considers a feature index $j$ and a split threshold $s$ to partition the data into two regions:

$$R_1(j, s) = \{\mathbf{x} \mid x_j \le s\} \quad \text{and} \quad R_2(j, s) = \{\mathbf{x} \mid x_j > s\}$$

To find the optimal parameter pair $(j, s)$, the algorithm minimizes the sum of squared residuals (Mean Squared Error framework):

$$\min_{j, s} \left[ \sum_{\mathbf{x}_i \in R_1(j, s)} (y_i - c_1)^2 + \sum_{\mathbf{x}_i \in R_2(j, s)} (y_i - c_2)^2 \right]$$

where $c_1$ and $c_2$ are the sample means of the target values in $R_1(j, s)$ and $R_2(j, s)$, respectively. This search is repeated across all available dimensions at each node to locate the absolute best partition.

### 2.3. Variance Reduction Metric
An alternative but mathematically equivalent optimization objective is maximizing **Variance Reduction**. The variance reduction achieved by splitting a parent node $P$ into left ($L$) and right ($R$) children is defined as:

$$\Delta \text{Var} = \text{Var}(P) - \left( \frac{N_L}{N_P} \text{Var}(L) + \frac{N_R}{N_P} \text{Var}(R) \right)$$

where the localized variance for any arbitrary node $A$ containing $N_A$ elements is computed as:

$$\text{Var}(A) = \frac{1}{N_A} \sum_{i \in A} (y_i - \bar{y}_A)^2$$

### 2.4. Stopping and Regularization Criteria
To prevent the tree from splitting down to single data instances (which yields a training error of zero but severe overfitting), structural regularization constraints are enforced:
* **`max_depth`:** Limits the maximum number of structural levels from the root node to a leaf.
* **`min_samples_split`:** Restricts a node from splitting if its sample size falls below a minimum threshold.
* **`min_samples_leaf`:** Ensures that a split is only permitted if both resulting child nodes contain at least a specified minimum number of samples.

---

## 3. Algorithm Description

1. **Root Optimization:** Initialize the root node containing the entire training dataset.
2. **Recursive Partitioning Execution:** For each active un-split node:
    * Loop through each feature dimension $j$ (or a random subspace governed by `max_features`).
    * For each continuous feature, sort the unique observed values to evaluate them as candidate split thresholds $s$.
    * Calculate the resulting Mean Squared Error or Variance Reduction for each candidate pair $(j, s)$.
    * Select the optimal feature and split threshold that maximizes variance reduction.
3. **Child Node Delegation:** Partition the node's samples into left and right child nodes based on the condition $x_j \le s$.
4. **Termination Check:** Repeat the partitioning step recursively for all child nodes until any of the stopping criteria (`max_depth`, `min_samples_split`, or `min_samples_leaf`) are met, or if no split yields a positive reduction in variance.
5. **Inference Mapping:** To predict a target value for an unseen vector $\mathbf{x}$, route the instance down the tree based on the conditional feature splits until it reaches a terminal leaf node, and return the stored region mean $c_m$.