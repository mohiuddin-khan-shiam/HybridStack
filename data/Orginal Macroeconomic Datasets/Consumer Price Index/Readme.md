# Consumer Price Index (CPI) Analysis

## Overview

The **Consumer Price Index (CPI)** is one of the most widely used measures of inflation and changes in the cost of living. It tracks the average change over time in the prices paid by consumers for a representative basket of goods and services.

Governments, central banks, economists, researchers, investors, and businesses rely on CPI to evaluate inflationary trends, adjust wages and benefits, formulate monetary policy, and assess economic conditions.

In the United States, CPI is published monthly by the U.S. Bureau of Labor Statistics (BLS). The most commonly used CPI series in economic research is:

**Consumer Price Index for All Urban Consumers (CPI-U)**

FRED Series Code:

**CPIAUCSL**

---

# Table of Contents

* [Overview](#overview)
* [What is CPI?](#what-is-cpi)
* [Economic Importance](#economic-importance)
* [How CPI is Constructed](#how-cpi-is-constructed)
* [Types of CPI](#types-of-cpi)
* [Mathematical Formulation](#mathematical-formulation)
* [Example Calculations](#example-calculations)
* [Inflation Measurement](#inflation-measurement)
* [Why CPI Matters](#why-cpi-matters)
* [Data Sources](#data-sources)
* [Applications](#applications)
* [Advantages](#advantages)
* [Limitations](#limitations)
* [Python Examples](#python-examples)
* [Research Applications](#research-applications)
* [Related Economic Indicators](#related-economic-indicators)
* [References](#references)
* [Citation](#citation)
* [License](#license)

---

# What is CPI?

The Consumer Price Index measures the average price change over time for a basket of consumer goods and services purchased by households.

The basket includes categories such as:

* Food and beverages
* Housing
* Transportation
* Medical care
* Education
* Recreation
* Apparel
* Energy
* Communication

CPI serves as a key indicator of inflation and purchasing power.

---

# Economic Importance

CPI plays a central role in economic analysis because it helps quantify changes in the cost of living.

### Rising CPI

A rising CPI generally indicates:

* Increasing inflation
* Higher consumer prices
* Reduced purchasing power

---

### Falling CPI

A falling CPI may indicate:

* Deflation
* Weak demand
* Economic slowdown

---

### Stable CPI

A stable CPI suggests:

* Price stability
* Controlled inflation
* Predictable economic conditions

---

# How CPI is Constructed

The U.S. Bureau of Labor Statistics follows a multi-stage process:

## Step 1: Consumer Expenditure Survey

The BLS identifies what households purchase and how much they spend.

---

## Step 2: Basket Construction

A representative basket of goods and services is developed.

Examples include:

| Category       | Example Items       |
| -------------- | ------------------- |
| Food           | Bread, milk, fruits |
| Housing        | Rent, utilities     |
| Transportation | Gasoline, vehicles  |
| Healthcare     | Medical services    |
| Education      | Tuition fees        |

---

## Step 3: Price Collection

Thousands of prices are collected monthly from:

* Retail stores
* Service providers
* Online retailers
* Housing units

---

## Step 4: Weight Assignment

Each category receives a weight based on consumer spending patterns.

Example:

| Category       | Weight (%) |
| -------------- | ---------- |
| Housing        | 34         |
| Transportation | 17         |
| Food           | 14         |
| Healthcare     | 8          |
| Recreation     | 5          |

---

## Step 5: Index Computation

The weighted average price changes are aggregated into the CPI index.

---

# Types of CPI

## CPI-U

Consumer Price Index for All Urban Consumers.

Coverage:

* Approximately 93% of the U.S. population

Most widely used CPI measure.

---

## CPI-W

Consumer Price Index for Urban Wage Earners and Clerical Workers.

Commonly used for:

* Social Security adjustments
* Wage contracts

---

## Core CPI

Excludes:

* Food
* Energy

Purpose:

* Measures underlying inflation trends
* Reduces short-term volatility

FRED Code:

CPILFESL

---

## Headline CPI

Includes all categories, including food and energy.

Often referenced in media reports.

---

# Mathematical Formulation

## Laspeyres Price Index

CPI is primarily based on a modified Laspeyres index:

[
CPI_t
=====

\frac{
\sum P_t Q_0
}{
\sum P_0 Q_0
}
\times 100
]

Where:

| Symbol | Meaning              |
| ------ | -------------------- |
| (P_t)  | Current period price |
| (P_0)  | Base period price    |
| (Q_0)  | Base period quantity |

---

## Interpretation

* CPI = 100 → Base period
* CPI > 100 → Prices increased
* CPI < 100 → Prices decreased

---

# Example Calculations

## Example Basket

| Item     | Base Price | Current Price |
| -------- | ---------- | ------------- |
| Bread    | $2.00      | $2.40         |
| Milk     | $3.00      | $3.60         |
| Gasoline | $2.50      | $3.25         |

Total Base Cost:

[
$7.50
]

Total Current Cost:

[
$9.25
]

CPI:

[
\frac{9.25}{7.50}
\times 100
==========

123.33
]

Interpretation:

Consumer prices increased by approximately 23.3%.

---

# Inflation Measurement

## Year-over-Year Inflation

The most common inflation measure:

[
Inflation_t
===========

\frac{
CPI_t - CPI_{t-12}
}{
CPI_{t-12}
}
\times 100
]

---

## Example

| Year | CPI |
| ---- | --- |
| 2024 | 300 |
| 2025 | 309 |

Inflation:

[
\frac{309 - 300}{300}
\times 100
==========

3.0%
]

---

## Month-over-Month Inflation

[
\frac{
CPI_t - CPI_{t-1}
}{
CPI_{t-1}
}
\times 100
]

Used for short-term inflation monitoring.

---

# Why CPI Matters

## Central Banks

Central banks monitor CPI to:

* Guide interest-rate decisions
* Assess inflationary pressures
* Maintain price stability

---

## Governments

Governments use CPI for:

* Policy evaluation
* Benefit adjustments
* Economic planning

---

## Businesses

Businesses use CPI to:

* Adjust pricing strategies
* Forecast costs
* Negotiate contracts

---

## Investors

Investors monitor CPI because inflation influences:

* Bond yields
* Equity valuations
* Currency markets
* Commodity prices

---

# Data Sources

## U.S. Bureau of Labor Statistics (BLS)

Official CPI source.

Website:

https://www.bls.gov/cpi

---

## Federal Reserve Economic Data (FRED)

Popular CPI series:

| Series     | Code     |
| ---------- | -------- |
| CPI-U      | CPIAUCSL |
| Core CPI   | CPILFESL |
| Energy CPI | CPIENGSL |
| Food CPI   | CPIFABSL |

Website:

https://fred.stlouisfed.org

---

## U.S. Federal Reserve

Provides:

* Inflation reports
* Monetary policy assessments
* Economic projections

Website:

https://www.federalreserve.gov

---

## OECD

Provides international CPI statistics.

Website:

https://www.oecd.org

---

## World Bank

Provides global inflation datasets.

Website:

https://www.worldbank.org

---

# Applications

## 1. Inflation Forecasting

CPI is frequently used as:

* Prediction target
* Explanatory variable
* Benchmark inflation measure

Models include:

* ARIMA
* SARIMA
* VAR
* Prophet
* LSTM
* GRU
* Transformers

---

## 2. Monetary Policy Analysis

Researchers examine:

* Interest-rate responses
* Inflation targeting
* Central bank credibility

---

## 3. Cost-of-Living Analysis

Used for:

* Wage negotiations
* Pension adjustments
* Living cost comparisons

---

## 4. Financial Market Research

Applications include:

* Bond pricing
* Inflation-linked securities
* Real return calculations

---

# Advantages

## Widely Recognized

One of the most trusted inflation measures globally.

---

## Long Historical Series

Provides decades of consistent data.

---

## Comprehensive Coverage

Captures broad consumer spending patterns.

---

## Policy Relevance

Used extensively by governments and central banks.

---

# Limitations

## Substitution Bias

Consumers may switch to cheaper alternatives, which CPI may not fully capture.

---

## Quality Adjustment Challenges

Product improvements may affect price comparisons.

---

## Housing Measurement Issues

Some economists argue housing costs may be imperfectly represented.

---

## Average Consumer Assumption

CPI reflects average spending patterns and may not represent all households equally.

---

# Python Examples

## Download CPI Data from FRED

```python
import pandas_datareader.data as web

cpi = web.DataReader(
    "CPIAUCSL",
    "fred",
    start="2000-01-01"
)

print(cpi.head())
```

---

## Calculate Year-over-Year Inflation

```python
import pandas_datareader.data as web

cpi = web.DataReader(
    "CPIAUCSL",
    "fred",
    start="2000-01-01"
)

inflation_yoy = (
    cpi.pct_change(12) * 100
)

print(inflation_yoy.tail())
```

---

## Plot CPI

```python
import pandas_datareader.data as web
import matplotlib.pyplot as plt

cpi = web.DataReader(
    "CPIAUCSL",
    "fred",
    start="2000-01-01"
)

cpi.plot(figsize=(12,6))
plt.title("Consumer Price Index (CPI)")
plt.ylabel("Index")
plt.show()
```

---

# Research Applications

Common research questions include:

## Inflation Forecasting

* Can machine learning improve CPI forecasts?
* Which macroeconomic indicators best predict inflation?

---

## Monetary Policy

* How do interest-rate changes affect CPI?
* What is the lag between policy actions and inflation outcomes?

---

## Labor Economics

* How does inflation affect wages?
* How do CPI changes influence household purchasing power?

---

## Financial Economics

* How does CPI affect Treasury yields?
* How do inflation shocks impact stock returns?

---

# Related Economic Indicators

| Indicator                   | FRED Code |
| --------------------------- | --------- |
| CPI                         | CPIAUCSL  |
| Core CPI                    | CPILFESL  |
| PCE Price Index             | PCEPI     |
| Core PCE                    | PCEPILFE  |
| Federal Funds Rate          | FEDFUNDS  |
| Unemployment Rate           | UNRATE    |
| Producer Price Index        | PPIACO    |
| 10-Year Treasury Yield      | GS10      |
| 10-Year Breakeven Inflation | T10YIE    |
| 5Y5Y Forward Inflation Rate | T5YIFR    |

---

# References

## U.S. Bureau of Labor Statistics

Consumer Price Index Program

https://www.bls.gov/cpi

---

## Federal Reserve Bank of St. Louis (FRED)

Consumer Price Index for All Urban Consumers (CPIAUCSL)

https://fred.stlouisfed.org/series/CPIAUCSL

---

## Federal Reserve Board

Inflation and Monetary Policy Reports

https://www.federalreserve.gov

---

## OECD Inflation Statistics

https://www.oecd.org

---

## World Bank Inflation Database

https://www.worldbank.org

---

## Mankiw, N. Gregory

Macroeconomics.

---

## Blanchard, Olivier

Macroeconomics.

---

## Mishkin, Frederic S.

The Economics of Money, Banking, and Financial Markets.

---

# Citation

If using this repository in academic work, please cite:

```bibtex
@misc{cpi_analysis,
  title={Consumer Price Index Analysis},
  author={Your Name},
  year={2026},
  note={Inflation Measurement and Economic Analysis}
}
```

---

# License

This project is licensed under the MIT License.

---

# Acknowledgments

* U.S. Bureau of Labor Statistics (BLS)
* Federal Reserve Bank of St. Louis (FRED)
* Federal Reserve System
* OECD
* World Bank
* Researchers in inflation economics and macroeconomic forecasting
