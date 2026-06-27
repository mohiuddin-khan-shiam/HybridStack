# K-Nearest Neighbors (KNN) Regressor

## 1. Background and Context
The **K-Nearest Neighbors (KNN)** algorithm is an intuitive, non-parametric, instance-based supervised learning method introduced by Evelyn Fix and Joseph Hodges in 1951, and later expanded by Thomas Cover and Peter Hart. It is classified as a "lazy learner" because it does not learn an explicit discriminative or generative model function during a training phase. Instead, the training step simply stores the historical dataset instances.

In regression tasks, KNN predicts the target value of a novel query instance based on the local similarity of its closest historical sample neighbors in the multi-dimensional feature space. Because it avoids establishing a rigid global mathematical relationship, KNN is highly adaptable to highly non-linear local data manifolds. It is exceptionally straightforward to understand and configure, though it can become computationally expensive during testing phase operations as the dataset size grows.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Distance Metrics
The foundation of KNN relies on evaluating geometric distance between a new query instance $\mathbf{x}_q$ and an existing database instance $\mathbf{x}_i$. The generalized distance metric used is the Minkowski distance of order $p$:

$$D(\mathbf{x}_q, \mathbf{x}_i) = \left( \sum_{j=1}^{d} |x_{q,j} - x_{i,j}|^p \right)^{\frac{1}{p}}$$

Where $d$ is the total number of feature dimensions. Two specific variants of this formula are frequently utilized:
* **Manhattan Distance ($p=1$):** Measures absolute coordinate grid deviations:
  $$D_{\text{manhattan}}(\mathbf{x}_q, \mathbf{x}_i) = \sum_{j=1}^{d} |x_{q,j} - x_{i,j}|$$
* **Euclidean Distance ($p=2$):** Measures ordinary straight-line distance:
  $$D_{\text{euclidean}}(\mathbf{x}_q, \mathbf{x}_i) = \sqrt{\sum_{j=1}^{d} (x_{q,j} - x_{i,j})^2}$$

### 2.2. Neighbor Neighborhood Assignment
Given a target count parameter $k$ (`n_neighbors`), the algorithm evaluates distances from $\mathbf{x}_q$ to all stored entries. It then identifies the subset $N_k(\mathbf{x}_q)$ containing the $k$ training points that have the smallest computed distance values.

### 2.3. Prediction Aggregation and Weight Strategies
Once the neighborhood $N_k(\mathbf{x}_q)$ is established, the target continuous prediction $\hat{y}_q$ is formulated using one of two primary strategy methods:

#### Uniform Weights
Every neighbor within the isolated subset contributes equally to the inference target, which is calculated as the simple arithmetic mean:

$$\hat{y}_q = \frac{1}{k} \sum_{\mathbf{x}_i \in N_k(\mathbf{x}_q)} y_i$$

#### Distance Weights
Neighbors located closer to the query point exert a greater mathematical influence on the prediction than those farther away. The weight $w_i$ assigned to an instance $i$ is inversely proportional to its distance:

$$w_i = \frac{1}{D(\mathbf{x}_q, \mathbf{x}_i) + \delta}$$

Where $\delta$ is an extremely small constant value (e.g., $10^{-10}$) inserted to prevent a division-by-zero error if a query sample perfectly overlaps a training point. The prediction is computed as a weighted average:

$$\hat{y}_q = \frac{\sum_{\mathbf{x}_i \in N_k(\mathbf{x}_q)} w_i y_i}{\sum_{\mathbf{x}_i \in N_k(\mathbf{x}_q)} w_i}$$

---

## 3. Algorithm Description

1. **Instance Storage (Training):** Store the complete feature matrix $\mathbf{X}$ and corresponding continuous target vector $\mathbf{y}$.
2. **Distance Assessment (Inference):** For an incoming unseen query feature vector $\mathbf{x}_q$:
    * Compute the distance metric (Manhattan, Euclidean, or general Minkowski based on $p$) between $\mathbf{x}_q$ and every stored training instance $\mathbf{x}_i$.
3. **Neighborhood Sorting:** Sort the calculated distance arrays in ascending order and extract the top $k$ corresponding nearest training samples to form the localized neighborhood subset $N_k(\mathbf{x}_q)$.
4. **Target Estimation Output:** * If `weights='uniform'`, compute the unweighted sample mean of the target variables within $N_k(\mathbf{x}_q)$.
    * If `weights='distance'`, calculate the inverse distance weights for each neighbor, and return their normalized weighted target summation.