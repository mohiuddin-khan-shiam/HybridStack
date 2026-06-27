# ElasticNet Regression (L1 and L2 Regularization)

## 1. Background and Context
**ElasticNet Regression** is a regularized linear regression technique proposed by Zou and Hastie in 2005. It was designed to overcome critical limitations found in both Lasso ($L_1$) and Ridge ($L_2$) regularization schemes when handling complex, high-dimensional datasets.

While Lasso Regression performs automatic feature selection by driving irrelevant feature weights exactly to zero, it exhibits two notable draw-backs:
* When the number of features $p$ is greater than the number of samples $n$, Lasso selects at most $n$ variables before saturating.
* If there is a group of highly correlated variables, Lasso tends to select only one variable from the group and completely ignore the others, which can cause erratic coefficient estimates.

Conversely, Ridge Regression handles multicollinearity smoothly by shrinking coefficients of correlated variables together, but it is incapable of reducing any coefficient to exactly zero, resulting in non-sparse models. ElasticNet fundamentally resolves these shortcomings by introducing a convex combination of both $L_1$ and $L_2$ penalties into the objective optimization function. This allows the model to maintain the feature selection capabilities of Lasso while inheriting the stability and grouping effect of Ridge.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Linear Model Definition
In a standard multiple linear regression model, the continuous target variable $y_i$ for a given instance $i$ is modeled as a linear combination of its input feature vector $\mathbf{x}_i \in \mathbb{R}^p$ and a weight vector $\boldsymbol{\beta} \in \mathbb{R}^p$:

$$y_i = \beta_0 + \sum_{j=1}^{p} \beta_j x_{ij} + \epsilon_i$$

Where $\beta_0$ represents the intercept term, $\beta_j$ represents the coefficient for feature $j$, and $\epsilon_i$ represents the random residual error.

### 2.2. Regularized Objective Function
ElasticNet modifies the standard Ordinary Least Squares (OLS) optimization problem by applying both penalties. Assuming the input features have been centered (allowing the isolation of $\beta_0$), the ElasticNet optimization criterion minimizes the regularized loss function:

$$\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n} \sum_{i=1}^{n} \left( y_i - \sum_{j=1}^{p} \beta_j x_{ij} \right)^2 + \lambda \left( \rho \sum_{j=1}^{p} |\beta_j| + \frac{1 - \rho}{2} \sum_{j=1}^{p} \beta_j^2 \right) \right\}$$

In compact matrix notation, this is expressed as:

$$\min_{\boldsymbol{\beta}} \left\{ \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|_2^2 + \alpha \rho \|\boldsymbol{\beta}\|_1 + \frac{\alpha (1 - \rho)}{2} \|\boldsymbol{\beta}\|_2^2 \right\}$$

Where:
* $n$ represents the total number of training samples.
* $\mathbf{y} \in \mathbb{R}^n$ is the target vector and $\mathbf{X} \in \mathbb{R}^{n \times p}$ is the feature design matrix.
* $\alpha$ (or $\lambda$) $\ge 0$ is the total regularization strength parameter. When $\alpha = 0$, the function reverts to an Ordinary Least Squares estimator.
* $\rho \in [0, 1]$ is the mixing parameter (often named `l1_ratio`). 
  * $\rho = 1$ simplifies the problem into pure Lasso Regression.
  * $\rho = 0$ simplifies the problem into pure Ridge Regression.
  * $0 < \rho < 1$ implements the hybrid ElasticNet approach.

### 2.3. Geometric Interpretation and Grouping Effect
Geometrically, the constraint region of ElasticNet combines the sharp corners of the Lasso diamond with the smooth, rounded contours of the Ridge hypersphere. 

The mathematical consequence of this hybrid constraint is known as the **grouping effect**. If two features $x_i$ and $x_j$ are highly correlated such that $\rho_{\text{corr}} \to 1$, their corresponding coefficients $\beta_i$ and $\beta_j$ will behave similarly. For a pure Lasso model, the allocation can be unstable; however, under ElasticNet, the difference between their coefficients is bounded by the $L_2$ penalty term, ensuring they are adjusted in tandem rather than forcing one arbitrarily to zero.

### 2.4. Optimization and Soft-Thresholding
Because the absolute value function in the $L_1$ penalty is non-differentiable at $\beta_j = 0$, ElasticNet cannot be computed using closed-form linear matrix conversions. Instead, it is solved using cyclical **Coordinate Descent** optimization.

Holding all other coefficients fixed, the coordinate update for a specific coefficient $\beta_j$ is given by applying a modified soft-thresholding operator:

$$\hat{\beta}_j = \frac{S_{\alpha \rho}\left( \sum_{i=1}^{n} x_{ij} \left( y_i - \sum_{k \neq j} \beta_k x_{ik} \right) \right)}{1 + \alpha(1 - \rho)}$$

where $S_z(w) = \text{sign}(w) \max(|w| - z, 0)$ represents the soft-thresholding operation that shrinks coefficients or snaps them to zero.

---

## 3. Algorithm Description

1. **Feature Standardization:** Standardize independent features to exhibit a mean of 0 and a variance of 1. Because regularization uniform penalties ($\sum |\beta_j|$ and $\sum \beta_j^2$) depend directly on coefficient scale, unscaled feature columns distort optimization constraints.
2. **Hyperparameter Workspace Mapping:** Set up an experimental multi-dimensional search grid mapping values for global regularization strength ($\alpha$) and mixing balance ratios ($\rho$).
3. **Cross-Validation Optimization Phase:** For each distinct pair $(\alpha, \rho)$ in the search grid, partition the training data into $K$ cross-validation folds:
    * Isolate $K-1$ training partitions and utilize cyclical coordinate descent to iteratively minimize the hybrid objective function until convergence limits are achieved.
    * Compute out-of-fold performance against the isolated validation fold using Mean Squared Error (MSE).
4. **Optimal Tuning Target Selection:** Determine the specific combination of hyperparameters maximizing model validation stability (or minimizing mean cross-validation error).
5. **Final Matrix Fitting:** Fit a final ElasticNet regression model instance against the full training sequence utilizing the determined optimal parameters.
6. **Inference Prediction:** For any incoming unseen evaluation matrix $\mathbf{X}_{\text{test}}$, apply identical historical scaling configurations and compute estimated target vectors via matrix operation:
   $$\hat{\mathbf{y}}_{\text{test}} = \mathbf{X}_{\text{test}}\hat{\boldsymbol{\beta}}_{\text{elastic\_net}}$$