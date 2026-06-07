# 10-Year Treasury Yield Analysis

## Overview

The **10-Year Treasury Yield** is one of the most important benchmark interest rates in global financial markets. It represents the annualized yield investors receive from holding a U.S. Treasury security with a maturity of ten years.

The 10-Year Treasury Yield serves as a critical indicator of:

* Economic growth expectations
* Inflation expectations
* Monetary policy outlook
* Financial market sentiment
* Borrowing costs throughout the economy

Because U.S. Treasury securities are backed by the full faith and credit of the United States government, the 10-Year Treasury Yield is widely considered a benchmark "risk-free" interest rate and is extensively used in academic research, investment management, and economic policymaking.

The Federal Reserve Bank of St. Louis publishes the series through FRED under the identifier **GS10**.

---

# Table of Contents

* [Overview](#overview)
* [What is the 10-Year Treasury Yield?](#what-is-the-10-year-treasury-yield)
* [Economic Significance](#economic-significance)
* [How Treasury Yields Work](#how-treasury-yields-work)
* [Factors Affecting Treasury Yields](#factors-affecting-treasury-yields)
* [Mathematical Concepts](#mathematical-concepts)
* [Example Calculations](#example-calculations)
* [Why It Matters](#why-it-matters)
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

# What is the 10-Year Treasury Yield?

The 10-Year Treasury Yield is the return an investor earns by purchasing and holding a 10-year U.S. Treasury note.

Treasury notes are debt securities issued by the U.S. Department of the Treasury to finance government operations and expenditures.

The yield reflects:

* Market interest rates
* Inflation expectations
* Economic growth expectations
* Supply and demand for government debt

Because Treasury securities are considered among the safest investments globally, the 10-Year Treasury Yield serves as a benchmark rate for many financial products.

---

# Economic Significance

The 10-Year Treasury Yield influences numerous sectors of the economy.

## Housing Market

Mortgage rates are closely linked to the 10-Year Treasury Yield.

When Treasury yields rise:

* Mortgage rates often increase
* Housing affordability decreases
* Home demand may weaken

When Treasury yields fall:

* Mortgage rates typically decline
* Borrowing becomes cheaper
* Housing demand may increase

---

## Corporate Finance

Businesses use Treasury yields as a benchmark when issuing:

* Corporate bonds
* Commercial paper
* Long-term debt instruments

Higher Treasury yields generally increase borrowing costs.

---

## Equity Markets

The yield affects stock valuations because it influences:

* Discount rates
* Future cash flow valuations
* Investor risk preferences

Rising yields often pressure growth stocks, while falling yields may support higher equity valuations.

---

## Government Borrowing

Treasury yields directly affect:

* Federal borrowing costs
* Debt servicing expenses
* Fiscal sustainability

---

# How Treasury Yields Work

Bond prices and yields move inversely.

## Relationship

| Bond Price | Yield     |
| ---------- | --------- |
| Increases  | Decreases |
| Decreases  | Increases |

Example:

If demand for Treasury bonds rises:

* Bond prices increase
* Yields fall

If demand falls:

* Bond prices decrease
* Yields rise

---

# Factors Affecting Treasury Yields

## Inflation Expectations

Higher expected inflation generally leads to higher Treasury yields because investors require compensation for reduced purchasing power.

---

## Federal Reserve Policy

Federal Reserve actions influence yields through:

* Federal Funds Rate decisions
* Quantitative Easing (QE)
* Quantitative Tightening (QT)
* Forward guidance

---

## Economic Growth

Strong economic growth often pushes yields higher because investors anticipate:

* Higher inflation
* Increased borrowing demand
* Tighter monetary policy

---

## Global Market Conditions

Treasury yields are affected by:

* Geopolitical events
* Financial crises
* International capital flows
* Currency market movements

---

## Supply and Demand

Increased issuance of Treasury securities may place upward pressure on yields, while strong investor demand may lower yields.

---

# Mathematical Concepts

## Yield to Maturity (YTM)

The yield to maturity represents the annualized return earned if a bond is held until maturity.

General formula:

[
P
=

\sum_{t=1}^{n}
\frac{C}{(1+y)^t}
+
\frac{F}{(1+y)^n}
]

Where:

| Symbol | Meaning           |
| ------ | ----------------- |
| P      | Bond Price        |
| C      | Coupon Payment    |
| F      | Face Value        |
| y      | Yield to Maturity |
| n      | Number of Periods |

---

## Real Yield Approximation

Real yield can be approximated as:

[
Real\ Yield
\approx
Nominal\ Yield
--------------

Inflation\ Rate
]

Example:

| Variable       | Value |
| -------------- | ----- |
| Treasury Yield | 4.5%  |
| Inflation      | 2.5%  |

[
Real\ Yield
===========

## 4.5%

# 2.5%

2.0%
]

---

# Example Calculations

## Example 1: Bond Yield

Assume:

| Parameter    | Value  |
| ------------ | ------ |
| Face Value   | $1,000 |
| Coupon Rate  | 4%     |
| Market Price | $950   |

Because the bond trades below par value, the effective yield exceeds the coupon rate.

---

## Example 2: Yield Spread

Suppose:

| Instrument       | Yield |
| ---------------- | ----- |
| 2-Year Treasury  | 3.5%  |
| 10-Year Treasury | 4.5%  |

Yield spread:

[
4.5%
----

# 3.5%

1.0%
]

A positive spread generally indicates normal economic expectations.

---

# Why It Matters

## Policymakers

Governments and central banks monitor Treasury yields to assess:

* Market confidence
* Inflation expectations
* Economic outlook

---

## Investors

Portfolio managers use Treasury yields for:

* Asset valuation
* Portfolio construction
* Risk management
* Benchmarking

---

## Researchers

Economists analyze Treasury yields to study:

* Business cycles
* Monetary policy transmission
* Recession forecasting
* Financial market behavior

---

# Data Sources

## Federal Reserve Economic Data (FRED)

Series:

* GS10

Description:

* 10-Year Treasury Constant Maturity Rate

Link:

https://fred.stlouisfed.org/series/GS10

---

## U.S. Department of the Treasury

Provides:

* Daily Treasury yield curve rates
* Historical yield data
* Auction results

Link:

https://home.treasury.gov

---

## Federal Reserve Board

Provides:

* Interest rate reports
* Monetary policy data
* Economic analyses

Link:

https://www.federalreserve.gov

---

## Bloomberg Terminal

Provides:

* Real-time Treasury yields
* Yield curve analytics
* Historical financial data

---

## Refinitiv Workspace

Provides:

* Fixed-income datasets
* Bond market analytics
* Yield curve information

---

# Applications

## 1. Macroeconomic Forecasting

Treasury yields are commonly used in forecasting models for:

* GDP growth
* Inflation
* Recessions
* Interest rates

---

## 2. Recession Prediction

The yield curve derived from Treasury yields is a well-known recession indicator.

Common spread:

[
10Y - 2Y
]

An inverted yield curve has historically preceded many recessions.

---

## 3. Financial Modeling

Treasury yields are used as:

* Risk-free rates
* Discount rates
* Benchmark rates

Applications include:

* CAPM
* DCF valuation
* Bond pricing

---

## 4. Portfolio Management

Used for:

* Duration management
* Fixed-income allocation
* Risk assessment
* Performance benchmarking

---

# Advantages

## Highly Liquid Market

Treasury securities are among the most actively traded assets globally.

---

## Reliable Benchmark

Widely accepted as a proxy for the risk-free rate.

---

## Forward-Looking

Reflects market expectations about future economic conditions.

---

## Long Historical Record

Provides decades of data for research and analysis.

---

# Limitations

## Influenced by Multiple Factors

Treasury yields reflect:

* Inflation expectations
* Risk sentiment
* Monetary policy
* Global capital flows

Therefore, interpretation may not always be straightforward.

---

## Market Distortions

Large-scale asset purchases by central banks can affect market pricing.

---

## Not a Direct Economic Forecast

Yields contain market expectations but do not guarantee future outcomes.

---

# Python Examples

## Download GS10 Data from FRED

```python
import pandas_datareader.data as web

gs10 = web.DataReader(
    "GS10",
    "fred",
    start="2000-01-01"
)

print(gs10.head())
```

---

## Plot Treasury Yield

```python
import pandas_datareader.data as web
import matplotlib.pyplot as plt

gs10 = web.DataReader(
    "GS10",
    "fred",
    start="2000-01-01"
)

gs10.plot(figsize=(12,6))
plt.title("10-Year Treasury Yield (GS10)")
plt.ylabel("Percent")
plt.show()
```

---

## Calculate Yield Spread

```python
import pandas_datareader.data as web

gs10 = web.DataReader("GS10", "fred")
gs2 = web.DataReader("GS2", "fred")

spread = gs10 - gs2

print(spread.tail())
```

---

# Research Applications

Common research questions include:

## Monetary Policy

* How do Federal Reserve decisions affect Treasury yields?
* How effective is forward guidance?

---

## Recession Forecasting

* Can yield curve inversions predict recessions?
* What spread provides the best forecasting performance?

---

## Financial Markets

* How do Treasury yields affect stock returns?
* What is the relationship between yields and volatility?

---

## Machine Learning

Treasury yields are frequently used as features in:

* LSTM models
* GRU models
* XGBoost
* Random Forest
* Transformer architectures

---

# Related Economic Indicators

| Indicator                    | FRED Code |
| ---------------------------- | --------- |
| Federal Funds Rate           | FEDFUNDS  |
| 2-Year Treasury Yield        | GS2       |
| 3-Month Treasury Bill Rate   | TB3MS     |
| 10-Year Treasury Yield       | GS10      |
| 30-Year Treasury Yield       | GS30      |
| CPI                          | CPIAUCSL  |
| Core CPI                     | CPILFESL  |
| 10-Year Breakeven Inflation  | T10YIE    |
| 5-Year Breakeven Inflation   | T5YIE     |
| 5Y5Y Forward Inflation Rate  | T5YIFR    |
| Effective Federal Funds Rate | DFF       |

---

# References

## Federal Reserve Bank of St. Louis (FRED)

10-Year Treasury Constant Maturity Rate (GS10)

https://fred.stlouisfed.org/series/GS10

---

## U.S. Department of the Treasury

Daily Treasury Yield Curve Rates

https://home.treasury.gov

---

## Federal Reserve Board

Interest Rate Statistics and Monetary Policy Reports

https://www.federalreserve.gov

---

## Fabozzi, Frank J.

Bond Markets, Analysis, and Strategies.

---

## Mishkin, Frederic S.

The Economics of Money, Banking, and Financial Markets.

---

## Campbell, Lo, and MacKinlay

The Econometrics of Financial Markets.

---

# Citation

If using this repository in academic work, please cite:

```bibtex
@misc{gs10_analysis,
  title={10-Year Treasury Yield Analysis},
  author={Your Name},
  year={2026},
  note={Benchmark Long-Term Interest Rate and Economic Indicator}
}
```

---

# License

This project is licensed under the MIT License.

---

# Acknowledgments

* Federal Reserve Bank of St. Louis (FRED)
* U.S. Department of the Treasury
* Federal Reserve System
* Financial economists and fixed-income researchers
* Global investment and policy communities
