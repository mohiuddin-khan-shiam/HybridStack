# Ridge Regression (L2 Regularization)

## 1. Background and Context
**Ridge Regression**, also known as Tikhonov regularization, is an extension of Ordinary Least Squares (OLS) linear regression designed to address the problem of multicollinearity and overfitting in parametric models. Introduced independently by Hoerl and Kennard in 1970, Ridge Regression modifies the linear model's objective function by introducing an $L_2$ penalty term.

In standard OLS estimation, when independent features are highly correlated (multicollinearity), the variance of the estimated regression coefficients becomes extremely high. This leads to unstable models where a small change in the training data can cause massive shifts in coefficient magnitudes and signs, resulting in poor generalization on unseen data. Ridge Regression resolves this structural issue by imposing a penalty on the size of the coefficients, shrinking them toward zero (but never exactly to zero). This introduces a small amount of bias into the model but yields a substantial reduction in variance, producing more stable and reliable predictions.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Linear System Formulation
Consider a standard linear relationship where a continuous target variable $y_i$ is modeled as a linear combination of an input feature vector $\mathbf{x}_i \in \mathbb{R}^p$ plus an error term $\epsilon_i$:

$$y_i = \beta_0 + \sum_{j=1}^{p} \beta_j x_{ij} + \epsilon_i$$

In matrix notation, for a dataset containing $n$ samples, the relationship is expressed as:

$$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

Where $\mathbf{y} \in \mathbb{R}^n$ is the target vector, $\mathbf{X} \in \mathbb{R}^{n \times (p+1)}$ is the design matrix containing feature values (with a column of ones for the intercept), $\boldsymbol{\beta} \in \mathbb{R}^{p+1}$ is the coefficient vector, and $\boldsymbol{\epsilon}$ is the residual error vector.

### 2.2. Regularized Objective Function
While Ordinary Least Squares minimizes the Residual Sum of Squares (RSS), Ridge Regression adds a penalty proportional to the square of the magnitude of the weight vector (excluding the intercept $\beta_0$). The optimization problem is written as:

$$\min_{\boldsymbol{\beta}} \left\{ \sum_{i=1}^{n} \left( y_i - \beta_0 - \sum_{j=1}^{p} \beta_j x_{ij} \right)^2 + \alpha \sum_{j=1}^{p} \beta_j^2 \right\}$$

Assuming the design matrix columns have been centered (so the intercept $\beta_0 = \bar{y}$), the loss function can be compactly represented in matrix form:

$$\mathcal{L}(\boldsymbol{\beta}) = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T(\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) + \alpha \|\boldsymbol{\beta}\|_2^2$$

Where:
* $\alpha \ge 0$ is the regularization parameter (hyperparameter). When $\alpha = 0$, Ridge Regression collapses back into an Ordinary Least Squares estimator. As $\alpha \to \infty$, the penalty dominates, forcing $\boldsymbol{\beta} \to \mathbf{0}$.
* $\|\boldsymbol{\beta}\|_2^2 = \sum_{j=1}^{p} \beta_j^2$ represents the square of the $L_2$ norm of the coefficient vector.

### 2.3. Analytical Closed-Form Solution
A significant advantage of Ridge Regression is that its objective function remains convex and differentiable, meaning it retains an exact analytical closed-form solution. To derive the solution, we take the partial derivative of the loss function with respect to $\boldsymbol{\beta}$ and set it to zero:

$$\frac{\partial \mathcal{L}(\boldsymbol{\beta})}{\partial \boldsymbol{\beta}} = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) + 2\alpha \boldsymbol{\beta} = 0$$

$$- \mathbf{X}^T\mathbf{y} + \mathbf{X}^T\mathbf{X}\boldsymbol{\beta} + \alpha \boldsymbol{\beta} = 0$$

$$\left( \mathbf{X}^T\mathbf{X} + \alpha \mathbf{I} \right) \boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}$$

$$\hat{\boldsymbol{\beta}}_{\text{ridge}} = \left( \mathbf{X}^T\mathbf{X} + \alpha \mathbf{I} \right)^{-1} \mathbf{X}^T\mathbf{y}$$

Where $\mathbf{I}$ is the $(p \times p)$ identity matrix. In standard OLS regression, if features are multicollinear, $\mathbf{X}^T\mathbf{X}$ is singular or near-singular, making its inverse unstable. Adding the term $\alpha \mathbf{I}$ ensures that the matrix $(\mathbf{X}^T\mathbf{X} + \alpha \mathbf{I})$ is strictly positive-definite and always invertible, guaranteeing a stable numerical calculation.

---

## 3. Algorithm Description

1. **Data Standardization:** Scale input features to have a mean of 0 and a variance of 1. Because the $L_2$ penalty treats all coefficients uniformly ($\sum \beta_j^2$), features with larger raw magnitudes will be disproportionately penalized if not standardized beforehand.
2. **Hyperparameter Definition:** Set up a search grid of candidate regularization strengths ($\alpha$).
3. **Cross-Validation Evaluation:** For each candidate value of $\alpha$, split the training dataset into $K$ cross-validation folds:
    * Train the model closed-form linear solver on $K-1$ folds: $\hat{\boldsymbol{\beta}} = \left( \mathbf{X}^T\mathbf{X} + \alpha \mathbf{I} \right)^{-1} \mathbf{X}^T\mathbf{y}$.
    * Evaluate model accuracy on the remaining validation fold using Mean Squared Error (MSE).
4. **Optimal Parameter Selection:** Identify the $\alpha$ value that yields the lowest average cross-validation error.
5. **Final Model Fitting:** Train a final Ridge Regression model using the optimal $\alpha$ on the entire training dataset.
6. **Inference Prediction:** For any incoming unseen instance feature matrix $\mathbf{X}_{\text{test}}$, generate continuous target estimations using the matrix transformation:
   $$\hat{\mathbf{y}}_{\text{test}} = \mathbf{X}_{\text{test}}\hat{\boldsymbol{\beta}}_{\text{ridge}}$$