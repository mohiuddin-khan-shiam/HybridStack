# Random Forest Regressor with Hyperparameter Tuning

## 1. Background and Context
The **Random Forest** algorithm, introduced by Leo Breiman in 2001, is an ensemble learning method primarily used for classification and regression tasks. It operates by constructing a multitude of decision trees during training and outputting the mean or average prediction (for regression) of the individual trees.

Random Forests belong to the class of **Bagging (Bootstrap Aggregration)** algorithms. While individual decision trees are prone to high variance and overfitting, aggregating across a diverse forest significantly reduces variance without a substantial increase in bias. This makes Random Forest exceptionally robust against noise and multi-collinearity in features.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Bootstrap Aggregation (Bagging)
Given a training set $D = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, \mathbf{x}_n, y_n)\}$, bagging repeatedly selects a random sample with replacement from $D$ to create $B$ bootstrapped datasets $D_b$. For each dataset, a decision tree $\hat{f}_b$ is trained.

The final ensemble prediction for an unseen sample $\mathbf{x}$ is the average of all individual tree outputs:

$$\hat{f}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} \hat{f}_b(\mathbf{x})$$

### 2.2. Feature Subspace Sampling (The "Random" in Random Forest)
To decorrelate the trees, Random Forest adds an explicit layer of randomness: when splitting a node during tree construction, only a random subset of $m \le p$ features (where $p$ is the total number of features) is considered. 
* Typically, for regression, $m = \lfloor \frac{p}{3} \rfloor$ or $m = \sqrt{p}$ is chosen.

### 2.3. Mathematical Optimization of Splitting
For a given node, the algorithm searches for the optimal feature $j$ and split point $s$ that minimizes the Mean Squared Error (MSE). The split partitions the data into regions $R_1(j, s) = \{\mathbf{x} \mid x_j \le s\}$ and $R_2(j, s) = \{\mathbf{x} \mid x_j > s\}$.

The optimization objective is:

$$\min_{j, s} \left[ \sum_{\mathbf{x}_i \in R_1(j, s)} (y_i - \bar{y}_{R_1})^2 + \sum_{\mathbf{x}_i \in R_2(j, s)} (y_i - \bar{y}_{R_2})^2 \right]$$

Where $\bar{y}_{R_1}$ and $\bar{y}_{R_2}$ represent the sample mean of the target variable in regions $R_1$ and $R_2$ respectively.

---

## 3. Algorithm Description

1. **Initialization:** Define the forest size $B$ (number of estimators) and hyperparameter space (e.g., maximum depth, split criteria).
2. **Bootstrapping:** For $b = 1$ to $B$:
    * Draw a bootstrap sample $D_b$ of size $n$ from the training data $D$ with replacement.
3. **Tree Growth:** Grow a randomized decision tree $\hat{f}_b$ using $D_b$ by recursively repeating the following steps for each node until termination conditions (e.g., max depth, min samples leaf) are met:
    * Select $m$ variables at random from the total $p$ features.
    * Pick the best variable/split-point among the $m$ features according to the MSE minimization objective.
    * Split the node into two child nodes.
4. **Ensemble Inference:** Pass a new query vector $\mathbf{x}$ through all $B$ constructed trees and return the mathematical mean of the predictions.