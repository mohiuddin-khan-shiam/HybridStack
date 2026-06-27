# Light Gradient Boosting Machine (LightGBM) Regressor

## 1. Background and Context
**Light Gradient Boosting Machine (LightGBM)** is a highly efficient, high-performance gradient boosting framework developed by Microsoft in 2017. It is designed to handle large-scale datasets with high dimensionality while optimizing computational speed and memory usage. 

Traditional Gradient Boosted Decision Tree (GBDT) implementations evaluate all data instances for every feature split, creating computational bottlenecks when working with millions of samples. LightGBM fundamentally overcomes this limitation through two core innovative strategies:
* **Gradient-based One-Side Sampling (GOSS):** Retains instances with larger gradients and performs random sampling on instances with smaller gradients, drastically shrinking data size without compromising accuracy.
* **Exclusive Feature Bundling (EFB):** Combines mutually exclusive features (features that rarely take non-zero values simultaneously) to reduce the overall feature dimensionality.

Furthermore, unlike most traditional tree architectures that split trees level-wise (horizontal growth), LightGBM utilizes a leaf-wise (vertical growth) strategy, yielding deeper trees with lower loss optimization objectives.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Gradient-based One-Side Sampling (GOSS)
In GOSS, instances are ranked by the absolute value of their gradients. Let the training dataset have $n$ instances. The algorithm sorts the instances and selects the top $a \times 100\%$ instances with the largest gradients to form subset $A$. For the remaining $(1 - a) \times 100\%$ instances with smaller gradients, it randomly samples a subset $B$ of size $b \times n$. 

To compensate for the change in data distribution, instances in subset $B$ are amplified by a constant weight factor $\frac{1-a}{b}$ when computing information gain. The estimated variance gain $V_j(d)$ for feature $j$ at a split point $d$ is mathematically formulated as:

$$\tilde{V}_j(d) = \frac{1}{n} \left( \frac{\left( \sum_{i \in A_l} g_i + \frac{1-a}{b} \sum_{i \in B_l} g_i \right)^2}{n_l^j(d)} + \frac{\left( \sum_{i \in A_r} g_i + \frac{1-a}{b} \sum_{i \in B_r} g_i \right)^2}{n_r^j(d)} \right)$$

Where:
* $A_l = \{i \in A : x_{ij} \le d\}$ and $A_r = \{i \in A : x_{ij} > d\}$
* $B_l = \{i \in B : x_{ij} \le d\}$ and $B_r = \{i \in B : x_{ij} > d\}$
* $g_i$ represents the first-order gradient of the loss function.
* $n_l^j(d)$ and $n_r^j(d)$ are the counts of samples falling into the left and right partitions respectively.

### 2.2. Exclusive Feature Bundling (EFB)
High-dimensional data is often sparse. EFB groups mutually exclusive features into a single feature bundle. It maps features to different bins by adding an offset value to the original feature values. For instance, if Feature 1 takes values in $[0, 10)$ and Feature 2 takes values in $[0, 20)$, Feature 2 is transformed by adding an offset of 10, mapping its values to $[10, 30)$. The combined feature bundle maps across $[0, 30)$ without value collision.

### 2.3. Leaf-wise Tree Growth Strategy
Most GBDT frameworks grow trees level-by-level, which can be inefficient because it optimizes nodes with low variance gain. LightGBM adopts a leaf-wise strategy, finding the leaf node with the absolute maximum splitting gain among all active leaves, regardless of tree level depth.

$$\text{Leaf To Split} = \arg\max_{\text{leaf } m} \left[ \text{Gain}(m) \right]$$

While leaf-wise growth minimizes loss more effectively, it can result in highly complex, deep configurations. To mitigate overfitting, LightGBM introduces a structural constraint on the maximum number of leaves (`num_leaves`) and maximum depth (`max_depth`).

---

## 3. Algorithm Description

1. **Feature Optimization & Pre-processing:**
    * Group sparse, mutually exclusive features into continuous indices using Exclusive Feature Bundling (EFB).
    * Discretize continuous feature values into discrete bins (controlled by `max_bin`) to build histograms.
2. **Instance Selection via GOSS:**
    * Compute the loss gradient for every instance based on the prior boosting tree predictions.
    * Sort instances by absolute gradient values.
    * Retain the top $a \times 100\%$ instances, and randomly sample $b \times 100\%$ instances from the remaining lower-gradient collection.
3. **Leaf-wise Tree Construction:**
    * Initialize from the tree root node.
    * For each candidate leaf node, compute information split gains across feature histograms using the weighted GOSS optimization objective.
    * Select the single leaf node that yields the absolute maximum structural loss reduction and split it vertically.
    * Repeat until the total number of leaves matches `num_leaves` or the tree hits its `max_depth` restriction.
4. **Ensemble Weight Assembly:**
    * Update the target regression residual weights sequentially across boosting rounds. Stop when the total number of estimators (`n_estimators`) is met or early stopping is triggered.