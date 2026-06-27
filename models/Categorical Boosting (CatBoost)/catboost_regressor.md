# Categorical Boosting (CatBoost) Regressor

## 1. Background and Context
**CatBoost** (short for Categorical Boosting) is an advanced open-source gradient boosting framework developed by Yandex in 2017. While traditional Gradient Boosted Decision Tree (GBDT) algorithms like XGBoost and LightGBM excel at handling numerical data, they face substantial limitations when dealing with categorical features. Typically, users must apply manual preprocessing techniques—such as one-hot encoding or target encoding—which often leads to severe information loss, dimensionality explosion, or data leakage.

CatBoost introduces fundamental structural solutions to these challenges:
* **Ordered Target Encoding:** A mathematical method to transform categorical features into continuous numeric values without incurring target data leakage (look-ahead bias).
* **Symmetric Trees (Oblivious Trees):** A restriction where the same splitting criterion is chosen across an entire level of a tree, maximizing processing speed during execution and acting as an implicit regularization mechanism against overfitting.
* **Ordered Boosting:** A permutation-based training methodology designed to mitigate prediction shift—a type of bias inherent in classical gradient boosting algorithms caused by using the same data instances to estimate gradients and build tree structures.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Ordered Target Encoding
To convert a categorical feature $\tilde{x}_i$ into a continuous value, simple target encoding replaces the category with the average target value $\mathbb{E}[y \mid \tilde{x}_i]$. However, calculating this average directly on the training set introduces data leakage. CatBoost prevents this using **Ordered Target Encoding**, which processes instances sequentially over a random permutation $\sigma = (\sigma_1, \sigma_2, \dots, \sigma_n)$ of the training set.

For a categorical value belonging to the $i$-th instance in the permutation, the target encoding value $\hat{x}_{j, \sigma_i}$ is computed using only historical instances that precede it:

$$\hat{x}_{j, \sigma_i} = \frac{\sum_{j=1}^{i-1} \mathbb{I}(\tilde{x}_{\sigma_j, j} = \tilde{x}_{\sigma_i, j}) \cdot y_{\sigma_j} + p \cdot P}{\sum_{j=1}^{i-1} \mathbb{I}(\tilde{x}_{\sigma_j, j} = \tilde{x}_{\sigma_i, j}) + p}$$

Where:
* $\mathbb{I}(\cdot)$ is an indicator function returning 1 if the condition is satisfied, and 0 otherwise.
* $y_{\sigma_j}$ is the continuous target scalar of the historical instance.
* $P$ is a global prior value (typically the mean target value of the full dataset).
* $p$ is a prior weight parameter (a regularization term that prevents division by zero and stabilizes low-frequency categories).

### 2.2. Ordered Boosting and Prediction Shift Mitigation
In standard GBDT implementations, the gradient statistics used to fit a new tree $f_t$ are evaluated using the same samples that the preceding ensemble $F_{t-1}$ was trained on. This introduces an optimization bias known as *prediction shift*.

CatBoost handles this by maintaining multiple independent model structures $M_i$. To calculate the gradient step for sample $i$, CatBoost evaluates the residual using a model $M_i$ that was trained completely without sample $i$:

$$g_i = \left[ \frac{\partial L(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)} \right]_{F(\mathbf{x}) = M_i(\mathbf{x}_i)}$$

Because the sample was excluded from $M_i$, the gradient $g_i$ is unbiased, breaking the feedback loop that drives overfitting.

### 2.3. Oblivious (Symmetric) Trees
CatBoost utilizes oblivious trees as its weak base learners. In an oblivious tree, all nodes at the same depth level share identical splitting conditions (the same feature index and threshold boundary). 



As a result, a tree with depth $d$ has exactly $2^d$ leaves, and the index of the leaf containing any given sample can be calculated rapidly via bitwise operations. This structural uniformity guarantees predictable execution paths, lowering cache-miss bottlenecks during testing and production inference.

---

## 3. Algorithm Description

1. **Permutation Configuration:**
    * Generate multiple random permutations ($\sigma^{(1)}, \sigma^{(2)}, \dots$) of the training dataset. These permutations decouple the indices for both ordered target encoding and ordered boosting.
2. **Dynamic ordered Preprocessing:**
    * As the algorithm iterates through a permutation, convert categorical inputs into numerical features on-the-fly using the historical conditional target calculation.
3. **Symmetric Tree Construction via Ordered Boosting:** For each boosting iteration:
    * Compute the unshifted loss gradient statistics for each sample using the corresponding models trained on historical records.
    * Construct an oblivious tree by greedily evaluating potential splits. The chosen split must maximize the global objective gain uniformly across all active nodes at that depth level.
    * Fill all terminal leaves with optimal output prediction weights.
4. **Ensemble Aggregation:**
    * Scale the final symmetric tree outputs by the learning rate (`learning_rate`) and add them to the ensemble.
    * Repeat until the iteration count (`iterations`) is reached or early stopping constraints trigger.