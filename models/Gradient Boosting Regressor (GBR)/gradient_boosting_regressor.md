# Gradient Boosting Regressor

## 1. Background and Context
**Gradient Boosting** is an ensemble machine learning technique primarily used for regression and classification tasks. Originally formulated by Leo Breiman and fully developed by Jerome H. Friedman in 1999, Gradient Boosting produces a competitive predictive model in the form of an ensemble of weak prediction models, which are almost exclusively decision trees.

Unlike bagging techniques such as Random Forests—which build deep, independent trees in parallel—Gradient Boosting constructs shallow trees sequentially. Each new tree is designed to fit the negative gradient (the residuals) of the loss function evaluated at the current ensemble's predictions. By iteratively correcting the errors of preceding trees, the ensemble converts multiple weak learners into a single highly accurate strong learner.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Empirical Risk Minimization
The objective of a regression model is to find a function $\hat{F}(\mathbf{x})$ that maps an input vector $\mathbf{x}$ to a continuous target scalar $y$ by minimizing the expected value of a specified loss function $L(y, F(\mathbf{x}))$ over the joint distribution of the data:

$$F^* = rg\min_F \mathbb{E}_{X,Y} [L(Y, F(X))]$$

Given a finite training dataset $D = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_n, y_n)\}$, we minimize the empirical risk:

$$\mathcal{L}(F) = \sum_{i=1}^{n} L(y_i, F(\mathbf{x}_i))$$

For a standard regression task, the Mean Squared Error (MSE) loss function is frequently employed:

$$L(y_i, F(\mathbf{x}_i)) = rac{1}{2} (y_i - F(\mathbf{x}_i))^2$$

### 2.2. Gradient Descent in Functional Space
Instead of updating parameters in a traditional parameter space, Gradient Boosting performs gradient descent directly in the *function space*. At each step $m$, the model additions follow the negative gradient direction of the loss function.

The negative gradient (pseudo-residual) for instance $i$ at iteration $m$ is defined as:

$$r_{im} = -\left[ rac{\partial L(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)} ight]_{F(\mathbf{x}) = F_{m-1}(\mathbf{x})}$$

For an MSE loss function, this derivative simplifies neatly to the raw operational residual:

$$r_{im} = y_i - F_{m-1}(\mathbf{x}_i)$$

### 2.3. Base Learner Fitting and Step Length Optimization
A weak learner (base decision tree) $h_m(\mathbf{x})$ is trained using the training set $\{(\mathbf{x}_i, r_{im})\}_{i=1}^n$ to predict the pseudo-residuals. The terminal leaves of this tree partition the feature space into $J_m$ disjoint regions $R_{1m}, R_{2m}, \dots, R_{J_m, m}$. For each region, an optimal leaf value $\gamma_{jm}$ is computed to minimize the loss:

$$\gamma_{jm} = rg\min_{\gamma} \sum_{\mathbf{x}_i \in R_{jm}} L(y_i, F_{m-1}(\mathbf{x}_i) + \gamma)$$

For MSE loss, $\gamma_{jm}$ corresponds exactly to the mean of the pseudo-residuals assigned to that leaf region $R_{jm}$.

### 2.4. Regularization via Shrinkage
To prevent overfitting and enhance generalization, the ensemble update is scaled by a learning rate parameter $
u \in (0, 1]$, also known as the shrinkage factor:

$$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + 
u \sum_{j=1}^{J_m} \gamma_{jm} \mathbb{I}(\mathbf{x} \in R_{jm})$$

Where $\mathbb{I}(\cdot)$ is an indicator function evaluating to 1 if the condition is met and 0 otherwise.

---

## 3. Algorithm Description

1. **Initialization:** Initialize the base model with a constant value that minimizes the global loss function:
   $$F_0(\mathbf{x}) = rg\min_{\gamma} \sum_{i=1}^{n} L(y_i, \gamma)$$
   *(For MSE loss, this initializes to the sample mean of the target labels).*
2. **Sequential Iterations:** For $m = 1$ to $M$ (where $M$ is the number of estimators `n_estimators`):
    * Compute the pseudo-residuals $r_{im}$ for all training instances $i = 1, \dots, n$.
    * Fit a regression tree $h_m(\mathbf{x})$ to the pseudo-residuals $r_{im}$, yielding terminal leaf split regions $R_{jm}$ for $j = 1, \dots, J_m$.
    * Compute the optimal terminal leaf values $\gamma_{jm}$ for each region.
    * Update the aggregate model framework by scaling the new tree predictions with the shrinkage learning rate ($
u$):
      $$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + 
u \cdot h_m(\mathbf{x})$$
3. **Inference Output:** The final optimized regression model output for an unseen input vector $\mathbf{x}$ is given by $F_M(\mathbf{x})$.
