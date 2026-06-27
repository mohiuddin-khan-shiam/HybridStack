# Shapley Additive exPlanations (SHAP) & KernelSHAP

## 1. Introduction and Purpose of the Method
**Shapley Additive exPlanations (SHAP)** is a game-theoretic framework designed to explain the outputs of any machine learning model. Its primary purpose is to decompose a model's prediction for an individual instance into a sum of contributions from each input feature. By assigning an importance value—termed a **SHAP value**—to each feature, it quantifies how much the feature shifted the prediction away from the global baseline (expected) value. SHAP unifies local feature attribution methods under a single mathematically rigorous definition, bridging the gap between local explanations (why a specific instance received a prediction) and global interpretations (which features dominate across an entire population).

---

## 2. Background and Motivation
Complex machine learning systems, such as deep neural networks and ensemble boosted trees, offer high accuracy but function as opaque black boxes. Prior post-hoc explainability approaches, such as feature importance scores or early additive approximations, lacked theoretical validation and frequently violated fundamental properties like consistency or local accuracy. For instance, a model change that increased a feature's structural reliance could paradoxically lower its assigned global feature importance score.

To resolve these vulnerabilities, Lundberg and Lee (2017) adapted cooperative game theory principles originally conceptualized by Lloyd Shapley in 1953. In a game-theoretic context, features are viewed as **players** cooperating in a coalition to maximize a **payout** (the model's numerical prediction deviation). SHAP guarantees a fair allocation of this payout to each feature, eliminating heuristic inconsistencies.

---

## 3. Theoretical Foundation
SHAP belongs to the class of **additive feature attribution methods**. These frameworks define a local explanation as a linear function of binary variables representing feature presence or absence. The explanation model $g(z')$ approximates the original complex model $f(x)$ mapping an instance $x$ transformed into a binary coalition vector $x'$:

$$g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j$$

Where:
* $M$ is the maximum number of input features.
* $z' \in \{0, 1\}^M$ is a binary coalition vector where $1$ denotes a feature value is present and $0$ denotes it is absent.
* $\phi_j \in \mathbb{R}$ is the SHAP value assigned to feature $j$.
* $\phi_0 = \mathbb{E}[f(x)]$ is the base value, or the expected model output when no feature information is given.

Lundberg and Lee proved that any additive feature attribution method satisfying three fundamental mathematical properties uniquely defines its coefficients as Shapley values:

### I. Local Accuracy (Efficiency)
The sum of the local feature attributions must match the difference between the model output $f(x)$ and the base value $\phi_0$:
$$f(x) = g(x') = \phi_0 + \sum_{j=1}^{M} \phi_j$$

### II. Missingness
If a feature is absent from the input instance ($x'_j = 0$), its assigned attribution value must be zero:
$$\phi_j = 0$$

### III. Consistency (Monotonicity)
If a model structure changes such that the marginal contribution of feature $j$ increases or stays the same for all feature coalitions, its SHAP value cannot decrease:
$$\phi_j(f') \ge \phi_j(f) \quad \text{if} \quad f'(S \cup \{j\}) - f'(S) \ge f(S \cup \{j\}) - f(S) \quad \forall S \subseteq F \setminus \{j\}$$

---

## 4. Mathematical Formulation and Equations
The classical Shapley value calculation for a feature $j$ measures its weighted average marginal contribution across all possible feature subsets $S$ within the total feature set $F$:

$$\phi_j = \sum_{S \subseteq F \setminus \{j\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{j\}) - f_x(S) \right]$$

Where:
* $F$ is the complete set of all input features.
* $S$ is a subset of features excluding feature $j$.
* $|S|!$ represents the permutations of features present before adding $j$.
* $(|F| - |S| - 1)!$ represents the permutations of the remaining features after adding $j$.
* $|F|!$ is the total number of ways to sequence all features.
* $f_x(S)$ is the conditional expectation of the model prediction given the features in subset $S$, formulated as $\mathbb{E}[f(x) \mid x_S]$.

### KernelSHAP Formulation
Evaluating all $2^{|F|}$ feature combinations is computationally prohibitive. **KernelSHAP** avoids this exponential complexity by reformulating the problem as a weighted linear regression over binary feature coalitions. It computes the loss function using a specialized game-theoretic kernel, the **Shapley Kernel**:

$$\Omega(z') = \frac{|F| - 1}{\binom{|F|}{|z'|} |z'|(|F| - |z'|)}$$

Where $|z'| = \sum_{j=1}^M z'_j$ is the number of active features in the binary coalition vector. KernelSHAP fits a weighted linear model $g(z') = \phi_0 + \sum_{j=1}^M \phi_j z'_j$ by minimizing the squared error loss weighted by $\Omega(z')$. The resulting ordinary least squares regression coefficients yield the exact game-theoretic SHAP values.

---

## 5. Algorithm and Workflow

1. **Background Summarization:** Select a background reference dataset (e.g., using $K$-Means centroids) to compute marginal conditional expectations when a feature is toggled "off" ($z'_j = 0$).
2. **Coalition Sampling:** Generate a collection of binary coalition vectors $z'_m \in \{0, 1\}^M$ by sampling subset sizes randomly or exhaustively near the boundaries ($|z'| \in \{1, |F|-1\}$).
3. **Data Mapping:** Convert each binary coalition vector back into the original data space. For active features ($z'_j=1$), retain the query instance value $x_j$. For inactive features ($z'_j=0$), replace the missing index value with values sampled from the background reference dataset.
4. **Model Inference:** Run the mapped data instances through the predictive model $f(\cdot)$ to calculate the expected target adjustments.
5. **Kernel Weighting:** Calculate the structural weight $\Omega(z'_m)$ for each binary configuration using the Shapley Kernel equation.
6. **Regression Optimization:** Fit a weighted linear regression model on the generated dataset. Extract the resulting coefficients $\phi_j$ as the definitive SHAP feature attributions.

---

## 6. Key Assumptions
* **Feature Independence:** KernelSHAP assumes that features are independent when simulating missing values via background substitution. If features are highly correlated, replacing an inactive feature value can create unrealistic data instances that lie far outside the model's true data distribution, skewing the explanation.
* **Additivity:** It assumes the complex model's prediction can be locally approximated by a linear combination of feature impacts.

---

## 7. Input and Output Requirements

### Inputs
* **Predictive Model Function:** A callable function or method (`model.predict`) that returns numerical predictions for a given input matrix.
* **Background Dataset:** A representative sample of the feature space (typically $10$ to $100$ instances) used to simulate missing feature values.
* **Query Subsample Matrix:** The instances for which SHAP values and explanations are generated.

### Outputs
* **SHAP Values Matrix:** A multi-dimensional array of shape `(n_samples, n_features)` containing continuous feature attribution weights.
* **Base Value:** A baseline scalar value ($\phi_0$) representing the model's average prediction over the background reference dataset.

---

## 8. Advantages and Limitations

### Advantages
* **Solid Theoretical Foundation:** Backed by cooperative game theory, ensuring explanations satisfy local accuracy, missingness, and consistency properties.
* **Model-Agnostic:** KernelSHAP can explain any black-box machine learning model (e.g., linear models, tree ensembles, deep networks).
* **Local and Global Synthesis:** Aggregating local SHAP values provides global insights into feature importance and directionality without relying on heuristic metrics.

### Limitations
* **High Computational Cost:** Evaluating combinations scales with the feature space dimension, making KernelSHAP slow on high-dimensional data or large sample sizes.
* **Susceptibility to Extrapolation:** Dropping features via background sampling can synthesize out-of-distribution input combinations, leading to unpredictable model outputs.

---

## 9. Common Use Cases
* **Model Validation and Debugging:** Identifying if a model is relying on spurious correlations or biased shortcuts to make predictions.
* **Regulatory Compliance:** Providing transparent, case-by-case feature attributions in high-stakes fields like healthcare diagnostics, insurance underwriting, and credit scoring.
* **Scientific Discovery:** Uncovering multi-variable interactions and non-linear patterns within complex biomedical or financial feature spaces.

---

## 10. Important Parameters and Their Effects
* `nsamples` (Monte Carlo Sample Size): Controls the number of coalition vectors sampled during the linear regression stage. Lower values speed up computation but increase the variance of the calculated SHAP values. High values ensure stable and accurate explanations.
* `n_clusters` (K-Means Centroids Count): Determines the size of the background reference summary. Reducing the background dataset size using $K$-Means significantly speeds up the conditional expectation calculations in KernelSHAP.

---

## 11. Computational Complexity
The exact calculation of Shapley values requires evaluating all $2^{|F|}$ feature subsets, giving a computational complexity of $O(2^{|F|})$. KernelSHAP uses sampling to reduce this complexity to $O(N \cdot M \cdot S)$, where $N$ is the number of query samples to explain, $M$ is the number of input features, and $S$ is the number of Monte Carlo coalition samples (`nsamples`).

---

## 12. Best Practices and Practical Considerations
* **Standardize Background Data:** Always compress large training datasets into a concise background reference (e.g., $50$ to $100$ cluster centroids via $K$-Means) before running KernelSHAP to avoid prohibitively slow execution times.
* **Match Explainer to Model Type:** Use specialized explainer variants when available. For example, use **TreeSHAP** (`shap.TreeExplainer`) for decision trees and tree ensembles, or **DeepSHAP** for neural networks. These variants leverage internal model architectures to calculate exact SHAP values much faster than the model-agnostic `KernelExplainer`.
* **Export Visualizations Proactively:** When saving SHAP plots for publication, explicitly set the figure dimensions and context *before* invoking the plotting functions, and use vector formats like PDF or high-resolution rasters (e.g., 600 DPI PNG/TIFF) to ensure crisp details.