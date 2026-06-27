<div align="center">

# HybridStack

### Explainable Hybrid Ensemble for Accurate Inflation Forecasting with High-Frequency Macro-Financial Data

[![Paper](https://img.shields.io/badge/Paper-Array%20Journal-blue?style=for-the-badge&logo=elsevier)](https://www.sciencedirect.com/science/article/pii/S2590005626003267)
[![DOI](https://img.shields.io/badge/DOI-10.1016/j.array.2026.101003-green?style=for-the-badge)](https://doi.org/10.1016/j.array.2026.101003)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Citation](https://img.shields.io/badge/Cite-CITATION.cff-lightgrey?style=for-the-badge)](CITATION.cff)

</div>

---

## 📋 Overview

**HybridStack** is a novel **two-stage stacked generalization ensemble framework** for accurate and explainable inflation forecasting. It combines the complementary strengths of **XGBoost** (capturing nonlinear patterns) and **Ridge Regression** (capturing linear relationships) through an optimized stacking architecture with a **Ridge meta-learner**.

The framework leverages **Bayesian hyperparameter optimization** via Gaussian Processes with Expected Improvement acquisition, and employs **chronological K-fold cross-validation** to generate unbiased out-of-fold meta-features — preventing data leakage in time series contexts.

### Key Highlights

- 🏆 **Near-perfect R² = 0.999994** on 10-Year Breakeven Inflation Rate forecasting
- 📊 **9 macroeconomic indicators** from FRED (Federal Reserve Economic Data)
- 🔬 **16 baseline models** benchmarked across ML and DL paradigms
- 🧠 **3 XAI methods** (SHAP, LIME, PDP) for model interpretability
- 📈 **32 EDA analyses** for comprehensive data understanding
- ⚡ **Bayesian optimization** for efficient hyperparameter tuning

---

## 🏗️ Architecture

HybridStack uses a two-stage stacked generalization architecture:

```
                        ┌─────────────────────────────────────────┐
                        │           INPUT FEATURES (15)           │
                        │  9 macro indicators + 5 lags + rolling  │
                        └──────────────┬──────────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                      ▼
        ┌───────────────────┐                ┌───────────────────┐
        │   XGBoost (Base)  │                │  Ridge (Base)     │
        │   Nonlinear       │                │  Linear           │
        │   Patterns        │                │  Relationships    │
        └────────┬──────────┘                └────────┬──────────┘
                 │                                     │
                 │    Out-of-Fold Predictions           │
                 └──────────────┬──────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Ridge Meta-Learner  │
                    │   (Stage 2)           │
                    │                       │
                    │  ŷ = γ₁·f_XGB(x)     │
                    │     + γ₂·f_Ridge(x)  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   FINAL PREDICTION    │
                    └───────────────────────┘
```

---

## 📁 Repository Structure

```
HybridStack/
│
├── 📄 HybridStack.pdf                  # Published research paper
├── 📄 README.md                        # This file
├── 📄 LICENSE                          # Apache 2.0 License
├── 📄 CITATION.cff                     # Machine-readable citation
├── 📄 CONTRIBUTING.md                  # Contribution guidelines
├── 📄 CHANGELOG.md                     # Version history
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .gitignore                       # Git ignore rules
│
├── 📂 notebooks/                       # Main project code
│   └── HybridStack.ipynb              # Full end-to-end pipeline
│
├── 📂 models/                          # 16 model implementations
│   ├── HybridStack/                   # ⭐ Proposed model
│   ├── Ridge Regression (Ridge)/      # Base learner
│   ├── Extreme Gradient Boosting (XGBoost)/  # Base learner
│   ├── Random Forest (RF)/
│   ├── Light Gradient Boosting Machine (LightGBM)/
│   ├── Categorical Boosting (CatBoost)/
│   ├── Gradient Boosting Regressor (GBR)/
│   ├── Extremely Randomized Trees Regressor (ERTR)/
│   ├── Histogram-Based Gradient Boosting Regressor (HGBR)/
│   ├── K-Nearest Neighbors Regression (KNN)/
│   ├── Support Vector Regression (SVR)/
│   ├── Single Decision Tree Regressor (DTR)/
│   ├── Lasso Regression (Lasso)/
│   ├── ElasticNet Regression (EN)/
│   ├── Bidirectional Long Short-Term Memory (BiLSTM)/
│   └── Bidirectional Gated Recurrent Unit (Bi-GRU)/
│
├── 📂 data/                            # Datasets
│   ├── Dataset.md                     # Dataset documentation
│   ├── Orginal Macroeconomic Datasets/  # 10 FRED datasets
│   │   ├── 10-Year Breakeven Inflation Rate/  # Target variable
│   │   ├── Consumer Price Index/
│   │   ├── Real Gross Domestic Product/
│   │   ├── Unemployment Rate/
│   │   ├── Federal Funds Effective Rate/
│   │   ├── Personal Consumption Expenditures Index/
│   │   ├── 5-Year, 5-Year Forward Inflation Rate/
│   │   ├── Nominal Broad U.S. Dollar Index/
│   │   ├── Crude Oil Prices - West Texas Intermediate/
│   │   └── 10-Year Treasury Yield/
│   └── New Merged Dataset/            # Processed merged dataset
│       ├── code.py                    # Merging script
│       └── merged_dataset.csv         # Final merged data
│
├── 📂 eda/                             # 32 Exploratory Data Analyses
│   ├── Augmented Dickey-Fuller (ADF) Stationarity Analysis/
│   ├── Autocorrelation and Partial Autocorrelation Analysis (ACF - PACF)/
│   ├── Correlation Analysis/
│   ├── Time Series Decomposition Analysis/
│   ├── Principal Component Analysis (PCA)/
│   ├── Phillips Curve Analysis/
│   ├── Dynamic Time Warping (DTW) Analysis/
│   ├── Structural Break Detection Analysis/
│   └── ... (24 more analyses)
│
├── 📂 evaluation/                      # Evaluation metrics
│   ├── regression_metrics.py          # 7 metric implementations
│   └── regression_metrics.md          # Metric documentation
│
├── 📂 explainability/                  # XAI methods
│   ├── Shapley Additive exPlanations (SHAP)/
│   ├── Local Interpretable Model-agnostic Explanations (LIME)/
│   └── Partial Dependence Plots (PDP)/
│
├── 📂 ablation-studies/                # Ablation experiments
│   ├── 10_Year_Breakeven_Inflation_Rate.ipynb
│   ├── AI_Techniques_for_Time_Series_Forecasting_of_Inflation.ipynb
│   └── More Experiments.ipynb
│
├── 📂 drafts/                          # Initial draft notebooks
│   ├── Inflation.ipynb
│   ├── EDA Code.ipynb
│   ├── XAI.ipynb
│   ├── Code with Output.pdf
│   └── Output Description.pdf
│
└── 📂 .github/                         # GitHub community files
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml
```

> **Note:** Each subdirectory within `models/`, `eda/`, and `explainability/` contains a Python implementation (`.py`) and a Markdown documentation file (`.md`).

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/mohiuddin-khan-shiam/HybridStack.git
cd HybridStack
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import sklearn, xgboost, shap, lime; print('All dependencies installed successfully!')"
```

---

## 🚀 Usage

### Quick Start — Run the Full Pipeline

Open and execute the main notebook:

```bash
jupyter notebook notebooks/HybridStack.ipynb
```

This notebook contains the complete end-to-end pipeline:
1. **Data loading** — Loads the merged macroeconomic dataset
2. **Preprocessing** — Feature engineering, lag creation, train/test split
3. **Model training** — Trains all 16 baseline models + HybridStack
4. **Evaluation** — Computes all 7 regression metrics
5. **Visualization** — Generates comparison plots and result tables

### Running Individual Models

Each model in `models/` has a standalone Python implementation:

```bash
# Run the HybridStack model
python models/HybridStack/hybrid_stack.py

# Run XGBoost baseline
python "models/Extreme Gradient Boosting (XGBoost)/xgboost_regressor.py"

# Run Ridge Regression baseline
python "models/Ridge Regression (Ridge)/ridge_regression.py"
```

### Running EDA Analyses

Each analysis in `eda/` is self-contained:

```bash
# Run ADF stationarity test
python "eda/Augmented Dickey-Fuller (ADF) Stationarity Analysis/adf_stationarity_test.py"

# Run correlation analysis
python "eda/Correlation Analysis/correlation_analysis.py"
```

### Running Explainability Methods

```bash
# SHAP analysis
python "explainability/Shapley Additive exPlanations (SHAP)/shapley_additive_explanations.py"

# LIME analysis
python "explainability/Local Interpretable Model-agnostic Explanations (LIME)/local_interpretable_model_agnostic_explanations.py"

# Partial Dependence Plots
python "explainability/Partial Dependence Plots (PDP)/partial_dependence_plots.py"
```

---

## 📊 Datasets

The study uses **9 macroeconomic indicators** from the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) database to forecast the **10-Year Breakeven Inflation Rate (BEIR)** — the most widely used market-based measure of long-term U.S. inflation expectations.

| # | Feature | FRED Series | Frequency | Description |
|---|---------|------------|-----------|-------------|
| 🎯 | **10-Year Breakeven Inflation Rate** | T10YIE | Daily | Target variable (yield spread: nominal 10Y Treasury − 10Y TIPS) |
| 1 | 5Y-5Y Forward Inflation Rate | T5YIFR | Daily | Market-based long-term inflation expectations |
| 2 | Consumer Price Index | CPIAUCNS | Monthly | Consumer price level |
| 3 | Real GDP | GDPC1 | Quarterly | Real economic output |
| 4 | Unemployment Rate | UNRATE | Monthly | Labor market indicator |
| 5 | Federal Funds Rate | FEDFUNDS | Monthly | Monetary policy indicator |
| 6 | PCE Price Index | PCEPI | Monthly | Alternative inflation measure |
| 7 | Nominal Broad U.S. Dollar Index | DTWEXBGS | Daily | Currency strength |
| 8 | WTI Crude Oil Price | DCOILWTICO | Daily | Energy prices |
| 9 | 10-Year Treasury Yield | DGS10 | Daily | Long-term interest rates |

**Data range:** January 2, 2006 – October 1, 2024 (6,848 observations after daily resampling)

**Feature engineering:** 5 lag features + rolling mean → **15 total input features**

All original datasets are in `data/Orginal Macroeconomic Datasets/`, each with detailed documentation. The merged dataset is in `data/New Merged Dataset/`.

---

## 🤖 Models

### HybridStack (Proposed)

A two-stage stacked generalization ensemble:
- **Stage 1 (Base Learners):** XGBoost + Ridge Regression trained independently
- **Stage 2 (Meta-Learner):** Ridge Regression combines out-of-fold predictions
- **Optimization:** Bayesian hyperparameter tuning via Gaussian Processes

### Baseline Models (15)

| Category | Models |
|----------|--------|
| **Ensemble (Tree-Based)** | Random Forest, XGBoost, LightGBM, CatBoost, Gradient Boosting, Extra Trees, Histogram-Based Gradient Boosting |
| **Linear** | Ridge Regression, Lasso Regression, ElasticNet |
| **Instance-Based** | K-Nearest Neighbors, Support Vector Regression |
| **Tree-Based** | Decision Tree Regressor |
| **Deep Learning** | Bidirectional LSTM, Bidirectional GRU |

---

## 📈 Results

HybridStack achieves **near-perfect prediction accuracy**, significantly outperforming all 15 baseline models:

| Model | MSE | RMSE | MAE | MAPE (%) | R² |
|-------|-----|------|-----|----------|-----|
| **⭐ HybridStack** | **0.000000** | **0.000452** | **0.000248** | **0.0099** | **0.999994** |
| Ridge Regression | 0.0001 | 0.0113 | 0.0067 | 0.4288 | 0.9993 |
| HGBR | 0.0006 | 0.0242 | 0.0148 | 0.9646 | 0.9967 |
| XGBoost | 0.0006 | 0.0245 | 0.0146 | 0.9443 | 0.9966 |
| LightGBM | 0.0006 | 0.0251 | 0.0153 | 0.9767 | 0.9964 |
| CatBoost | 0.0007 | 0.0259 | 0.0169 | 1.0766 | 0.9962 |
| Extra Trees | 0.0008 | 0.0276 | 0.0152 | 0.9654 | 0.9957 |
| Random Forest | 0.0008 | 0.0288 | 0.0164 | 1.0480 | 0.9953 |

> **Key takeaway:** HybridStack's MAPE of **0.0099%** is approximately **43× better** than Ridge Regression alone (0.4288%), demonstrating the power of the stacking ensemble approach.

---

## 🔬 Evaluation Metrics

Seven regression metrics are used for comprehensive model evaluation:

| Metric | Description | Optimal |
|--------|-------------|---------|
| **MSE** | Mean Squared Error | → 0 |
| **RMSE** | Root Mean Squared Error | → 0 |
| **MAE** | Mean Absolute Error | → 0 |
| **MAPE** | Mean Absolute Percentage Error | → 0% |
| **sMAPE** | Symmetric MAPE | → 0% |
| **MASE** | Mean Absolute Scaled Error | < 1 |
| **R²** | Coefficient of Determination | → 1.0 |

Implementation and detailed documentation available in [`evaluation/`](evaluation/).

---

## 🧠 Explainability (XAI)

Three post-hoc interpretability methods provide transparency into model decisions:

| Method | Scope | Description |
|--------|-------|-------------|
| **[SHAP](explainability/Shapley%20Additive%20exPlanations%20(SHAP)/)** | Global + Local | Game-theoretic feature attribution via KernelSHAP |
| **[LIME](explainability/Local%20Interpretable%20Model-agnostic%20Explanations%20(LIME)/)** | Local | Perturbation-based surrogate linear models |
| **[PDP](explainability/Partial%20Dependence%20Plots%20(PDP)/)** | Global | Marginal effect of features on predictions |

---

## 📊 Exploratory Data Analysis

The `eda/` directory contains **32 comprehensive analyses**, each with standalone Python code and documentation:

<details>
<summary><b>Click to expand the full list of EDA analyses</b></summary>

| # | Analysis | Description |
|---|---------|-------------|
| 1 | ADF Stationarity Test | Unit root testing for time series stationarity |
| 2 | ACF & PACF | Autocorrelation and partial autocorrelation patterns |
| 3 | Bivariate Scatter Plots | Pairwise feature relationships |
| 4 | Bubble Charts | Multi-dimensional feature visualization |
| 5 | Categorical Bar Charts | Aggregated statistics visualization |
| 6 | Correlation Analysis | Feature correlation matrices and heatmaps |
| 7 | Cross-Correlation (CCF) | Lead-lag relationships between features |
| 8 | Box Plots | Distribution and outlier analysis |
| 9 | Violin Plots | Distribution shape analysis |
| 10 | Histograms & KDE | Frequency distributions |
| 11 | Double Exponential Smoothing | Trend and level smoothing |
| 12 | Dynamic Time Warping (DTW) | Time series similarity measurement |
| 13 | Hierarchical Clustering | Dendrogram-based feature grouping |
| 14 | Hodrick-Prescott Filter | Trend-cycle decomposition |
| 15 | KDE Analysis | Probability density estimation |
| 16 | Lag Plot Analysis | Serial dependence detection |
| 17 | Moving Averages | Trend extraction via smoothing |
| 18 | Network Correlation Graph | Graph-based correlation visualization |
| 19 | Pair Plots | Pairwise bivariate distributions |
| 20 | Peak & Trough Detection | Turning point identification |
| 21 | Phillips Curve | Inflation-unemployment relationship |
| 22 | PCA | Dimensionality reduction and variance analysis |
| 23 | Radar Charts | Multi-feature profile comparison |
| 24 | Rolling Window Analysis | Time-varying statistics |
| 25 | Rolling Variance Bands | Volatility trend analysis |
| 26 | Rolling vs. Expanding Windows | Statistical method comparison |
| 27 | Seasonal Heatmaps | Temporal pattern visualization |
| 28 | Structural Break Detection | Regime change identification |
| 29 | Time Series Decomposition | Trend, seasonal, residual separation |
| 30 | Resampling & Interpolation | Frequency conversion methods |
| 31 | Time Series Trend Analysis | Long-term trend extraction |
| 32 | Time Shifting & Lead-Lag | Temporal relationship analysis |

</details>

---

## 🔄 Reproducibility

To ensure full reproducibility of the results presented in the paper:

### 1. Environment Setup
```bash
# Create an isolated environment
python -m venv hybridstack-env
source hybridstack-env/bin/activate  # or hybridstack-env\Scripts\activate on Windows

# Install exact dependencies
pip install -r requirements.txt
```

### 2. Data
All datasets are included in the `data/` directory. No additional data download is required. The original FRED datasets are preserved with full provenance documentation.

### 3. Execution Order
For complete reproduction, follow this order:

```
1. Data Preparation    →  data/New Merged Dataset/code.py
2. Exploratory Analysis →  eda/ (any order)
3. Model Training      →  notebooks/HybridStack.ipynb
4. Individual Models   →  models/ (any order)
5. Evaluation          →  evaluation/regression_metrics.py
6. Explainability      →  explainability/ (any order)
7. Ablation Studies    →  ablation-studies/ (any order)
```

### 4. Hardware
The experiments were conducted using Google Colab with GPU (T4) acceleration. Deep learning models (BiLSTM, Bi-GRU) benefit from GPU availability, while ML models run efficiently on CPU.

### 5. Random Seeds
Random seeds are set within individual scripts for deterministic results. Minor variations may occur across different hardware/software configurations.

---

## 📝 How to Cite

If you use this code or find our work helpful, please cite our paper:

### Citation

> S.M.M.K. Shiam, M. Neela, A. Biswas, M.R. Chowdhury, HybridStack: Explainable hybrid ensemble for accurate inflation forecasting with high-frequency macro-financial data, *Array* 31 (2026) 101003. https://doi.org/10.1016/j.array.2026.101003

### BibTeX

```bibtex
@article{SHIAM2026101003,
  title     = {HybridStack: Explainable hybrid ensemble for accurate inflation forecasting with high-frequency macro-financial data},
  journal   = {Array},
  volume    = {31},
  pages     = {101003},
  year      = {2026},
  issn      = {2590-0056},
  doi       = {https://doi.org/10.1016/j.array.2026.101003},
  url       = {https://www.sciencedirect.com/science/article/pii/S2590005626003267},
  author    = {S. M. Mohiuddin Khan Shiam and Meherunnesa Neela and Amrijit Biswas and Mahdy Rahman Chowdhury}
}
```

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

```
Copyright 2026 S. M. Mohiuddin Khan Shiam, Meherunnesa Neela, Amrijit Biswas, Mahdy Rahman Chowdhury
```

---

## 👥 Authors

| Author | Role |
|--------|------|
| **S. M. Mohiuddin Khan Shiam** | Author |
| **Meherunnesa Neela** | Co-Author |
| **Amrijit Biswas** | Co-supervisor |
| **Mahdy Rahman Chowdhury** | supervisor |

### Contact

For questions, feedback, or collaboration inquiries, reach out to the author:

**S. M. Mohiuddin Khan Shiam**

[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--5504--2595-green?style=flat-square&logo=orcid)](https://orcid.org/0009-0005-5504-2595)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Profile-blue?style=flat-square&logo=google-scholar)](https://scholar.google.com/citations?view_op=list_works&hl=en&user=7gBr3qkAAAAJ)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Profile-00CCBB?style=flat-square&logo=researchgate)](https://www.researchgate.net/profile/S-M-Mohiuddin-Khan-Shiam)
[![GitHub](https://img.shields.io/badge/GitHub-mohiuddin--khan--shiam-181717?style=flat-square&logo=github)](https://github.com/mohiuddin-khan-shiam)

---

## 🙏 Acknowledgments

- Data sourced from the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) database
- Computational resources provided by [Google Colab](https://colab.research.google.com/)
- Built with open-source tools: [scikit-learn](https://scikit-learn.org/), [XGBoost](https://xgboost.readthedocs.io/), [SHAP](https://shap.readthedocs.io/), [LIME](https://lime-ml.readthedocs.io/), and the broader Python scientific computing ecosystem

---

<div align="center">

**⭐ If you find this work useful, please consider giving this repository a star! ⭐**

</div>