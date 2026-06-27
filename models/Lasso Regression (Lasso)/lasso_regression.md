# Lasso Regression (L1 Regularization)

## 1. Background and Context
**Lasso Regression**, short for *Least Absolute Shrinkage and Selection Operator*, is a regularized linear regression technique introduced by Robert Tibshirani in 1996. It was developed to address two critical limitations of Ordinary Least Squares (OLS) regression: prediction accuracy and model interpretability.

When a dataset contains a large number of features, OLS estimates often exhibit high variance, leading to poor generalization on unseen data. While alternative methods like Ridge Regression ($L_2$ regularization) reduce variance by shrinking coefficients toward zero, they keep all variables in the final model, making interpretation complex in high-dimensional spaces. Lasso Regression addresses this by adding an $L_1$ penalty term to the objective function. This penalty possesses unique geometric properties that can shrink some coefficients exactly to zero. Consequently, Lasso simultaneously performs regularization and automated feature selection, yielding sparser and more interpretable models.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Linear Model Definition
In a standard multiple linear regression setup, the continuous target variable $y_i$ for an instance $i$ is modeled as a linear combination of its input feature vector $\mathbf{x}_i \in \mathbb{R}^p$ and a set of weights $\boldsymbol{\beta} \in \mathbb{R}^p$:

$$y_i = \beta_0 + \sum_{j=1}^{p} \beta_j x_{ij} + \epsilon_i$$

Where $\beta_0$ represents the intercept term, $\beta_j$ represents the coefficient for feature $j$, and $\epsilon_i$ represents the random residual error.

### 2.2. Regularized Objective Function
Lasso Regression modifies the standard Residual Sum of Squares (RSS) objective function by adding a penalty proportional to the sum of the absolute values of the coefficients ($L_1$ norm). Assuming the input features have been centered (allowing us to omit the intercept $\beta_0$ from the penalty calculation), the Lasso optimization problem is formulated as:

$$\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n} \sum_{i=1}^{n} \left( y_i - \sum_{j=1}^{p} \beta_j x_{ij} \right)^2 + \alpha \sum_{j=1}^{p} |\beta_j| \right\}$$

In compact matrix notation, this is expressed as:

$$\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|_2^2 + \alpha \|\boldsymbol{\beta}\|_1 \right\}$$

Where:
* $n$ represents the total number of training samples.
* $\mathbf{y} \in \mathbb{R}^n$ is the target vector and $\mathbf{X} \in \mathbb{R}^{n \times p}$ is the feature design matrix.
* $\alpha \ge 0$ is the regularization parameter (hyperparameter). When $\alpha = 0$, the objective function reverts to Ordinary Least Squares. As $\alpha$ increases, the penalty forces more coefficients to become exactly zero.
* $\|\boldsymbol{\beta}\|_1 = \sum_{j=1}^{p} |\beta_j|$ represents the $L_1$ norm of the coefficient vector.

### 2.3. Geometric Interpretation and Feature Selection
The mathematical reason Lasso can force coefficients exactly to zero lies in the shape of its constraint region. The $L_1$ penalty can be rewritten as a constrained optimization problem: minimizing the RSS subject to $\sum |\beta_j| \le t$ for some threshold $t$. 

In a two-dimensional feature space, the constraint region forms a diamond with sharp corners situated on the coordinate axes. The contours of the RSS optimization function expand outward from the OLS estimate. The optimal Lasso solution is the point where an RSS contour first contacts the diamond constraint region. Because the diamond has sharp corners on the axes, the expanding contour frequently hits one of these corners first, setting the coordinate of the intersecting axis (and thus its corresponding feature coefficient) exactly to zero.

### 2.4. Optimization and Non-Differentiability
Unlike Ridge Regression, Lasso Regression cannot be solved analytically because the absolute value function $|\beta_j|$ introduces a non-differentiable kink at $\beta_j = 0$. Consequently, closed-form matrix inversions are unavailable. Optimization must be solved numerically using iterative algorithms, most commonly **Coordinate Descent** or Least Angle Regression (LARS). 

Under coordinate descent, the coefficient $\beta_j$ is updated iteratively while holding all other coefficients fixed, using the soft-thresholding operator:

$$\hat{\beta}_j = S_{\alpha}\left( \sum_{i=1}^{n} x_{ij} \left( y_i - \sum_{k \neq j} \beta_k x_{ik} \right) \right)$$

where $S_{\alpha}(z) = \text{sign}(z) \max(|z| - \alpha, 0)$.

---

## 3. Algorithm Description

1. **Feature Standardization:** Normalize all input features to have a mean of 0 and a variance of 1. Because the $L_1$ penalty treats all coefficients uniformly ($\sum |\beta_j|$), variables with larger raw scales will be penalized disproportionately if not standardized beforehand.
2. **Hyperparameter Configuration:** Define a search space grid of candidate regularization strengths ($\alpha$).
3. **Cross-Validation Search:** For each candidate value of $\alpha$, partition the data into $K$ cross-validation folds:
    * Isolate $K-1$ folds for training and use the coordinate descent algorithm to iteratively optimize the non-differentiable loss objective until convergence constraints are satisfied.
    * Measure performance on the remaining validation fold using Mean Squared Error (MSE).
4. **Optimal Selection:** Identify the $\alpha$ value that yields the lowest average cross-validation error.
5. **Final Fitting & Variable Selection:** Train the final Lasso model using the optimal $\alpha$ on the complete training dataset. Coefficients driven to exactly zero are dropped, isolating the selected feature subset.
6. **Inference Prediction:** For an unseen instance matrix $\mathbf{X}_{\text{test}}$, apply the identical scaling transformations and generate target values:
   $$\hat{\mathbf{y}}_{\text{test}} = \mathbf{X}_{\text{test}}\hat{\boldsymbol{\beta}}_{\text{lasso}}$$