# Support Vector Regression (SVR)

## 1. Background and Context
**Support Vector Regression (SVR)** is an adaptation of the Support Vector Machine (SVM) classification framework, developed by Vladimir Vapnik and his colleagues in 1996. While traditional linear regression models attempt to minimize the sum of squared errors between the predicted and true values, SVR operates on the principle of structural risk minimization rather than empirical risk minimization. 

The primary goal of SVR is to find a function $f(\mathbf{x})$ that has at most $\epsilon$ deviation from the actual targets $y_i$ for all training data points, while simultaneously remaining as flat as possible. This introduces a threshold called the **$\epsilon$-insensitive tube**, within which errors are ignored. By ignoring errors below a certain threshold and penalizing outliers, SVR builds an inherently robust model that resists noise and prevents overfitting. Additionally, through the use of the "Kernel Trick", SVR can effectively map non-linear input features into high-dimensional spaces where linear regression can be performed seamlessly.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. The $\epsilon$-Insensitive Loss Function
In SVR, the error of a prediction is evaluated using Vapnik's $\epsilon$-insensitive loss function $L_{\epsilon}(y, f(\mathbf{x}))$, which is mathematically defined as:

$$L_{\epsilon}(y, f(\mathbf{x})) = \begin{cases} 
0 & \text{if } |y - f(\mathbf{x})| \le \epsilon \\
|y - f(\mathbf{x})| - \epsilon & \text{otherwise}
\end{cases}$$

This means that any data instance falling inside the tube of radius $\epsilon$ around the regression line incurs zero penalty.

### 2.2. Primal Optimization Formulation
For a linear regression function $f(\mathbf{x}) = \langle\mathbf{w}, \mathbf{x}\rangle + b$, the objective of SVR is to maximize flatness (minimize $\frac{1}{2}\|\mathbf{w}\|^2$) subject to accuracy bounds. To allow for errors outside the $\epsilon$-tube, slack variables $\xi_i$ and $\xi_i^*$ are introduced, leading to the following optimization problem:

$$\min_{\mathbf{w}, b, \boldsymbol{\xi}, \boldsymbol{\xi}^*} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^{n} (\xi_i + \xi_i^*)$$

Subject to the constraints:
$$y_i - \langle\mathbf{w}, \mathbf{x}_i\rangle - b \le \epsilon + \xi_i$$
$$\langle\mathbf{w}, \mathbf{x}_i\rangle + b - y_i \le \epsilon + \xi_i^*$$
$$\xi_i, \xi_i^* \ge 0 \quad \text{for all } i = 1, 2, \dots, n$$

Where:
* $C > 0$ is a regularization parameter determining the trade-off between the flatness of $f(\mathbf{x})$ and the extent to which deviations larger than $\epsilon$ are tolerated.
* $\xi_i$ measures the error of data points above the $\epsilon$-tube.
* $\xi_i^*$ measures the error of data points below the $\epsilon$-tube.

### 2.3. Dual Formulation and the Kernel Trick
By applying Lagrange multipliers $\alpha_i$ and $\alpha_i^*$, the primal optimization problem is converted into its dual form, which is easier to solve and allows for non-linear mappings:

$$\max_{\boldsymbol{\alpha}, \boldsymbol{\alpha}^*} -\frac{1}{2} \sum_{i=1}^{n} \sum_{j=1}^{n} (\alpha_i - \alpha_i^*)(\alpha_j - \alpha_j^*) \langle\mathbf{x}_i, \mathbf{x}_j\rangle - \epsilon \sum_{i=1}^{n} (\alpha_i + \alpha_i^*) + \sum_{i=1}^{n} y_i(\alpha_i - \alpha_i^*)$$

Subject to constraints:
$$\sum_{i=1}^{n} (\alpha_i - \alpha_i^*) = 0$$
$$0 \le \alpha_i, \alpha_i^* \le C \quad \text{for all } i = 1, 2, \dots, n$$

When dealing with non-linear relationships, the inner product $\langle\mathbf{x}_i, \mathbf{x}_j\rangle$ is replaced by a non-linear mapping function into a feature space $\Phi(\mathbf{x})$, represented via a kernel function $K(\mathbf{x}_i, \mathbf{x}_j) = \langle\Phi(\mathbf{x}_i), \Phi(\mathbf{x}_j)\rangle$. The **Radial Basis Function (RBF)** kernel is the most popular choice:

$$K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2\right)$$

Where $\gamma$ defines how far the influence of a single training example reaches.

### 2.4. Final Regression Function
Once the dual parameters are solved, the weight vector can be expressed as $\mathbf{w} = \sum_{i=1}^{n} (\alpha_i - \alpha_i^*) \Phi(\mathbf{x}_i)$, leading to the final prediction function:

$$f(\mathbf{x}) = \sum_{i=1}^{n} (\alpha_i - \alpha_i^*) K(\mathbf{x}_i, \mathbf{x}) + b$$

The data instances with non-zero Lagrange coefficients $(\alpha_i - \alpha_i^* \neq 0)$ are located on or outside the boundary of the $\epsilon$-tube and are known as the **Support Vectors**.

---

## 3. Algorithm Description

1. **Feature Space Transformation:** Map the input training vectors $\mathbf{x}$ into a higher-dimensional space using the chosen kernel function $K(\mathbf{x}_i, \mathbf{x}_j)$ (e.g., RBF kernel).
2. **Gram Matrix Computation:** Evaluate the kernel inner product matrix for all pairs of training samples.
3. **Quadratic Programming Optimization:** Solve the dual maximization problem using optimization algorithms (such as Sequential Minimal Optimization, or SMO) to compute the optimal Lagrange multipliers $\alpha_i$ and $\alpha_i^*$.
4. **Support Vector Extraction:** Identify the data instances corresponding to $0 < \alpha_i, \alpha_i^* \le C$. These represent the support vectors that establish the regression boundaries.
5. **Intercept Computation:** Compute the bias term $b$ using the support vectors lying on the boundaries of the $\epsilon$-tube where slack is zero.
6. **Inference Prediction:** For any unseen incoming vector $\mathbf{x}$, compute its prediction by evaluating the kernel-weighted linear combination of the support vectors plus the intercept $b$.