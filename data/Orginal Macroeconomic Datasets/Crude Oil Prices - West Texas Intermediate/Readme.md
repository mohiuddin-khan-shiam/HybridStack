# Crude Oil Prices: West Texas Intermediate (WTI) Analysis

## Overview

**West Texas Intermediate (WTI)** is one of the world's most important crude oil benchmarks and serves as a key indicator of global energy market conditions. WTI crude oil is a high-quality, light, sweet crude oil primarily produced in the United States and traded extensively in commodity markets.

WTI prices influence:

* Global energy markets
* Inflation and consumer prices
* Transportation costs
* Industrial production
* Financial markets
* Monetary policy decisions

Researchers, investors, policymakers, and economists closely monitor WTI prices because crude oil is a critical input for economic activity and an important driver of inflationary pressures.

A widely used dataset for WTI prices is available through the Federal Reserve Bank of St. Louis (FRED) under the series:

**DCOILWTICO**

---

# Table of Contents

* [Overview](#overview)
* [What is West Texas Intermediate (WTI)?](#what-is-west-texas-intermediate-wti)
* [Historical Background](#historical-background)
* [Characteristics of WTI Crude Oil](#characteristics-of-wti-crude-oil)
* [Economic Importance](#economic-importance)
* [Price Determination](#price-determination)
* [Factors Affecting WTI Prices](#factors-affecting-wti-prices)
* [Mathematical Analysis](#mathematical-analysis)
* [Example Calculations](#example-calculations)
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

# What is West Texas Intermediate (WTI)?

WTI is a benchmark crude oil grade used for pricing oil in North America and many international markets.

Characteristics include:

* Light crude oil
* Low sulfur content
* High refining efficiency
* High gasoline yield

WTI futures contracts are primarily traded on the New York Mercantile Exchange (NYMEX).

---

# Historical Background

WTI became a global pricing benchmark due to:

* Significant U.S. oil production
* Development of futures markets
* Transparency of pricing mechanisms
* High-quality crude characteristics

Over time, WTI has become one of the most widely referenced oil price indicators in economic and financial research.

---

# Characteristics of WTI Crude Oil

## Light Crude Oil

WTI has a relatively low density.

Advantages:

* Easier refining process
* Higher production of gasoline and diesel

---

## Sweet Crude Oil

WTI contains low sulfur content.

Benefits:

* Lower refining costs
* Reduced environmental impact during processing

---

## Benchmark Status

WTI is commonly used for:

* Futures pricing
* Energy market analysis
* Economic forecasting
* Commodity investment decisions

---

# Economic Importance

Crude oil prices affect nearly every sector of the economy.

## Inflation

Higher oil prices often contribute to:

* Rising transportation costs
* Increased manufacturing expenses
* Higher consumer prices

---

## Economic Growth

Oil price shocks can significantly influence:

* GDP growth
* Industrial production
* Consumer spending

---

## Financial Markets

WTI prices impact:

* Energy sector stocks
* Commodity markets
* Bond markets
* Exchange rates

---

## Government Policy

Policymakers monitor oil prices to assess:

* Inflation risks
* Energy security
* Economic stability

---

# Price Determination

WTI prices are determined by supply and demand dynamics in global energy markets.

Major trading occurs through:

* Spot markets
* Futures contracts
* Options markets
* Energy exchanges

---

# Factors Affecting WTI Prices

## Global Demand

Demand increases with:

* Economic expansion
* Industrial production
* Transportation activity

Strong demand generally pushes prices higher.

---

## Supply Conditions

Supply depends on:

* OPEC production
* U.S. shale output
* Geopolitical disruptions
* Strategic petroleum reserves

Higher supply typically lowers prices.

---

## Geopolitical Events

Examples include:

* Armed conflicts
* Trade sanctions
* Political instability
* Supply chain disruptions

These events can cause substantial price volatility.

---

## Currency Movements

Since oil is priced in U.S. dollars:

* Stronger USD may reduce oil demand
* Weaker USD may increase oil demand

---

## Weather Events

Natural disasters can affect:

* Refinery operations
* Transportation infrastructure
* Production facilities

---

## Speculation and Futures Trading

Investor sentiment and futures positioning can influence short-term price movements.

---

# Mathematical Analysis

## Daily Return

One of the most common measures:

[
Return_t
========

\frac{
Price_t - Price_{t-1}
}{
Price_{t-1}
}
\times 100
]

---

## Log Return

Widely used in financial modeling:

[
r_t
===

\ln
\left(
\frac{P_t}{P_{t-1}}
\right)
]

Where:

* (P_t) = Current price
* (P_{t-1}) = Previous price

---

## Moving Average

Simple Moving Average (SMA):

[
SMA
===

\frac{
P_1 + P_2 + \cdots + P_n
}{n}
]

Used to smooth price fluctuations.

---

# Example Calculations

## Daily Percentage Change

Suppose:

| Day   | Price |
| ----- | ----- |
| Day 1 | $70   |
| Day 2 | $75   |

Then:

[
\frac{75 - 70}{70}
\times 100
==========

7.14%
]

Interpretation:

WTI increased by approximately 7.14%.

---

## Log Return

[
\ln
\left(
\frac{75}{70}
\right)
=======

0.069
]

Approximately 6.9%.

---

# Data Sources

## U.S. Energy Information Administration (EIA)

Official source for U.S. energy statistics.

Website:

https://www.eia.gov

---

## Federal Reserve Economic Data (FRED)

Series:

**DCOILWTICO**

Description:

Crude Oil Prices: West Texas Intermediate (WTI)

Website:

https://fred.stlouisfed.org/series/DCOILWTICO

---

## CME Group

Provides:

* WTI Futures Contracts
* Market specifications
* Trading information

Website:

https://www.cmegroup.com

---

## International Energy Agency (IEA)

Provides:

* Energy outlook reports
* Global oil market analysis

Website:

https://www.iea.org

---

## OPEC

Provides:

* Production statistics
* Oil market reports
* Supply assessments

Website:

https://www.opec.org

---

# Applications

## 1. Commodity Price Forecasting

WTI prices are commonly forecast using:

* ARIMA
* SARIMA
* GARCH
* Prophet
* LSTM
* GRU
* Transformer Models

---

## 2. Inflation Analysis

Researchers use WTI prices to explain:

* CPI movements
* Producer prices
* Inflation expectations

---

## 3. Financial Market Analysis

Applications include:

* Energy stock valuation
* Commodity portfolio management
* Risk analysis

---

## 4. Macroeconomic Research

Used to study:

* Economic growth
* Recessions
* Business cycles
* Monetary policy transmission

---

# Advantages

## Global Importance

One of the world's most influential commodity prices.

---

## High Liquidity

WTI futures are actively traded.

---

## Strong Economic Relevance

Closely connected to inflation and economic growth.

---

## Long Historical Record

Suitable for econometric and machine learning research.

---

# Limitations

## High Volatility

Oil prices can experience large short-term fluctuations.

---

## Geopolitical Sensitivity

Unexpected events can significantly impact prices.

---

## Structural Market Changes

Technological advances and policy shifts may alter historical relationships.

---

## Nonlinear Dynamics

Oil prices often exhibit:

* Regime changes
* Volatility clustering
* Structural breaks

---

# Python Examples

## Download WTI Data from FRED

```python
import pandas_datareader.data as web

wti = web.DataReader(
    "DCOILWTICO",
    "fred",
    start="2000-01-01"
)

print(wti.head())
```

---

## Calculate Daily Returns

```python
import pandas_datareader.data as web

wti = web.DataReader(
    "DCOILWTICO",
    "fred",
    start="2000-01-01"
)

returns = (
    wti.pct_change() * 100
)

print(returns.head())
```

---

## Calculate Log Returns

```python
import numpy as np
import pandas_datareader.data as web

wti = web.DataReader(
    "DCOILWTICO",
    "fred",
    start="2000-01-01"
)

log_returns = np.log(
    wti / wti.shift(1)
)

print(log_returns.head())
```

---

## Plot WTI Prices

```python
import pandas_datareader.data as web
import matplotlib.pyplot as plt

wti = web.DataReader(
    "DCOILWTICO",
    "fred",
    start="2000-01-01"
)

wti.plot(figsize=(12,6))
plt.title("WTI Crude Oil Prices")
plt.ylabel("USD per Barrel")
plt.show()
```

---

# Research Applications

Common research questions include:

## Commodity Forecasting

* Can machine learning improve oil price forecasts?
* Which macroeconomic variables predict oil prices best?

---

## Inflation Research

* How strongly do oil prices affect CPI?
* What is the pass-through effect of energy prices?

---

## Financial Economics

* How do oil shocks affect stock markets?
* How do oil prices influence bond yields?

---

## Energy Economics

* How effective are OPEC production cuts?
* How does shale production affect global markets?

---

# Related Economic Indicators

| Indicator                        | FRED Code    |
| -------------------------------- | ------------ |
| WTI Crude Oil                    | DCOILWTICO   |
| Brent Crude Oil                  | DCOILBRENTEU |
| CPI                              | CPIAUCSL     |
| Core CPI                         | CPILFESL     |
| PPI                              | PPIACO       |
| Industrial Production            | INDPRO       |
| Federal Funds Rate               | FEDFUNDS     |
| 10-Year Treasury Yield           | GS10         |
| S&P 500 Index                    | SP500        |
| Trade Weighted U.S. Dollar Index | DTWEXBGS     |

---

# References

## U.S. Energy Information Administration (EIA)

Official Energy Statistics

https://www.eia.gov

---

## Federal Reserve Bank of St. Louis (FRED)

Crude Oil Prices: West Texas Intermediate (WTI)

https://fred.stlouisfed.org/series/DCOILWTICO

---

## CME Group

WTI Crude Oil Futures

https://www.cmegroup.com

---

## International Energy Agency (IEA)

Oil Market Reports

https://www.iea.org

---

## OPEC

Annual Statistical Bulletin and Monthly Oil Market Reports

https://www.opec.org

---

## Hamilton, James D.

Oil and the Macroeconomy Since World War II.

Journal of Political Economy.

---

## Kilian, Lutz

Not All Oil Price Shocks Are Alike.

American Economic Review.

---

## Fattouh, Kilian, and Mahadeva

The Role of Oil Markets in Global Economic Activity.

---

# Citation

If using this repository in academic work, please cite:

```bibtex
@misc{wti_analysis,
  title={Crude Oil Prices: West Texas Intermediate (WTI) Analysis},
  author={Your Name},
  year={2026},
  note={Energy Economics, Commodity Markets, and Macroeconomic Research}
}
```

---

# License

This project is licensed under the MIT License.

---

# Acknowledgments

* U.S. Energy Information Administration (EIA)
* Federal Reserve Bank of St. Louis (FRED)
* CME Group
* International Energy Agency (IEA)
* OPEC
* Researchers in energy economics, commodity markets, and macroeconomic forecasting
