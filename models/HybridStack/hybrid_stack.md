# HybridStack Ensemble Model

## 1. Background and Context
[cite_start]**HybridStack** is an advanced, two-stage stacked generalization ensemble framework specifically designed to capture linear and nonlinear structural dependencies within high-dimensional feature spaces[cite: 7, 23, 63]. Introduced by Shiam et al. (2026)[cite_start], the architecture combines heterogeneous base learners from fundamentally different machine learning families to optimize predictive accuracy and variance reduction[cite: 7, 9, 23, 64, 202].

[cite_start]In complex predictive horizons, unique challenges such as sudden regime shifts, collinearity among features, and multi-scale temporal dependencies limit the effectiveness of individual parametric or non-parametric models[cite: 22, 54, 57]. [cite_start]Linear regularized models are structurally limited to linear transformations, while standalone tree-based ensembles often suffer from residual susceptibilities to extreme outlier distributions or parameter over-sensitivities[cite: 22, 36, 765]. [cite_start]HybridStack addresses this by combining an additive gradient-boosted tree ensemble (**XGBoost**) and a regularized linear regression framework (**Ridge Regression**) through a meta-learning architecture[cite: 23, 57, 202]. 

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. Base Learners Optimization Formulation
[cite_start]Let the training population be represented as $D = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$, where $\mathbf{x}_i \in \mathbb{R}^p$ denotes the $p$-dimensional input feature vector, and $y_i \in \mathbb{R}$ represents the corresponding continuous target scalar[cite: 263]. [cite_start]The first stage fits two independent, highly diversified learners[cite: 266, 309]:

#### Base Learner 1: XGBoost Regressor ($\mathcal{M}_{\text{XGB}}$)
[cite_start]An additive ensemble model built sequentially via gradient tree boosting[cite: 267]. Predictions are computed as:

$$f_{\text{XGB}}(\mathbf{x}) = \sum_{m=1}^{M} f_m(\mathbf{x}; \Theta_m)$$

[cite_start]where $f_m$ represents an individual regression tree parameterized by leaf scores and split indices $\Theta_m$[cite: 269, 271].

#### Base Learner 2: Ridge Regression ($\mathcal{M}_{\text{Ridge}}$)
[cite_start]A linear regression formulation incorporating an $L_2$ regularization penalty to manage collinearity and maintain parameter constraint stability[cite: 151, 272]. [cite_start]The coefficient weights are derived by solving[cite: 274, 275]:

$$\boldsymbol{\beta}^* = \arg\min_{\boldsymbol{\beta}} \left\{ \|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|_2^2 + \alpha_{\text{base}}\|\boldsymbol{\beta}\|_2^2 \right\}$$

where $\mathbf{X}$ is the design feature matrix, $\alpha_{\text{base}}$ controls regularization strength, and $\|\cdot\|_2$ denotes the standard Euclidean norm[cite: 275, 277].

### 2.2. Bayesian Hyperparameter Optimization
To maximize predictive diversity and accuracy without exhaustive grid searching, optimal values for the search spaces of both base models are determined independently using sequential Bayesian optimization over validation losses[cite: 23, 278, 280]. The optimal parameter maps $\lambda_k^*$ for a model $\mathcal{M}_k$ within its domain $A_k$ are extracted as follows[cite: 281]:

$$\lambda_k^* = \arg\min_{\lambda \in A_k} \mathbb{E}_{F} \left[ \mathcal{L}_{\text{CV}}(\mathcal{M}_k(\cdot; \lambda), D_{\text{train}}) \right]$$

[cite_start]where $\mathcal{L}_{\text{CV}}$ represents the average cross-validated loss computed over the validation folds $F$[cite: 282, 284].

### 2.3. Stacked Generalization via Out-of-Fold (OOF) Predictions
[cite_start]To protect the meta-learner from look-ahead bias and data leakage, the base frameworks are trained within a $K$-fold cross-validation scheme[cite: 23, 600]. [cite_start]Let $k(i)$ map to the specific isolated validation fold containing instance $i$[cite: 310]. [cite_start]The base learners generate out-of-fold predictions using parameter subsets trained strictly without that fold[cite: 310]:

$$z_{\text{XGB}, i} = f_{\text{XGB}}^{(-k(i))}(\mathbf{x}_i)$$

$$z_{\text{Ridge}, i} = f_{\text{Ridge}}^{(-k(i))}(\mathbf{x}_i)$$

[cite_start]These unbiased estimations are horizontally stacked to construct the new meta-feature matrix $\mathbf{Z}$[cite: 309, 310]:

$$\mathbf{Z} = \begin{bmatrix} \mathbf{z}_{\text{XGB}} & \mathbf{z}_{\text{Ridge}} \end{bmatrix} \in \mathbb{R}^{N \times 2}$$

### 2.4. Meta-Learner Integration
[cite_start]The final structural layer fits a second-stage Ridge regression meta-learner, $\mathcal{M}_{\text{meta}}$, using the meta-feature matrix $\mathbf{Z}$ and original targets $\mathbf{y}$[cite: 314]. [cite_start]The network derives combination weights $\boldsymbol{\gamma} \in \mathbb{R}^2$ by minimizing the regularized meta-loss criterion[cite: 315, 316]:

$$\boldsymbol{\gamma}^* = \arg\min_{\boldsymbol{\gamma}} \left\{ \|\mathbf{y} - \mathbf{Z}\boldsymbol{\gamma}\|_2^2 + \lambda_{\text{meta}}\|\boldsymbol{\gamma}\|_2^2 \right\}$$

where $\lambda_{\text{meta}}$ is the meta-regularization constraint[cite: 316, 319]. For any new unseen inference instance $\mathbf{x}_*$, the final optimized prediction ensemble maps as[cite: 319]:

$$\hat{y}_* = \gamma_1^* f_{\text{XGB}}(\mathbf{x}_*) + \gamma_2^* f_{\text{Ridge}}(\mathbf{x}_*)$$

---

## 3. Algorithm Description

1. **Hyperparameter Selection:** Map parameter spaces for XGBoost ($\mathcal{M}_{\text{XGB}}$) and Ridge Regression ($\mathcal{M}_{\text{Ridge}}$). [cite_start]Run sequential Bayesian optimization using Gaussian Processes to locate the configurations minimizing out-of-fold error metrics[cite: 23, 278, 280].
2. [cite_start]**Out-of-Fold Generation:** Partition the training input matrix $\mathbf{X}_{\text{train}}$ into $K$ non-shuffled chronological validation folds[cite: 500, 600]. For $k = 1$ to $K$:
    * [cite_start]Train optimized base instances $\mathcal{M}_{\text{XGB}}^{(k)}$ and $\mathcal{M}_{\text{Ridge}}^{(k)}$ on all segments except the active fold $k$[cite: 310].
    * [cite_start]Predict targets for the held-out fold $k$, saving outputs into the designated rows of vectors $\mathbf{z}_{\text{XGB}}$ and $\mathbf{z}_{\text{Ridge}}$[cite: 286, 310].
3. [cite_start]**Meta-Feature Matrix Construction:** Stack the complete out-of-fold vectors together to assemble the training meta-matrix $\mathbf{Z}_{\text{train}} = [\mathbf{z}_{\text{XGB}}, \, \mathbf{z}_{\text{Ridge}}]$[cite: 310, 311].
4. [cite_start]**Meta-Learning Finalization:** Train a regularized meta-Ridge regression model using $\mathbf{Z}_{\text{train}}$ against the baseline targets $\mathbf{y}_{\text{train}}$ to derive combination weights $\boldsymbol{\gamma}^*$[cite: 314, 315].
5. **Inference Execution:** For an incoming novel target row vector $\mathbf{x}_*$:
    * [cite_start]Route $\mathbf{x}_*$ through full-sample base models to generate predictions $f_{\text{XGB}}(\mathbf{x}_*)$ and $f_{\text{Ridge}}(\mathbf{x}_*)$[cite: 320].
    * [cite_start]Pass these outputs into the trained meta-learner model to obtain the final blended combination forecast[cite: 309, 320].