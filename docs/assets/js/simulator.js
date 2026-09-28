/**
 * HybridStack Interactive Live Forecasting Simulator
 * Emulates the 2-stage ensemble pipeline in-browser for interactive exploration
 */

const SIMULATOR_PRESETS = {
  surge2022: {
    name: "2022 Post-Pandemic Inflation Spike",
    description: "Geopolitical conflict drives crude oil above $110/bbl, global supply chains snarled, Fed begins historic rate hiking cycle.",
    oil: 114.8,
    yield10: 3.48,
    fedfunds: 1.58,
    dollar: 104.2,
    cpi: 296.3,
    unemp: 3.6,
    fwd5y5y: 2.42
  },
  crisis2008: {
    name: "2008 Great Financial Crisis",
    description: "Lehman Brothers collapse, systemic liquidity freeze in TIPS market, severe global recession and disinflation fear.",
    oil: 41.5,
    yield10: 2.25,
    fedfunds: 0.16,
    dollar: 84.8,
    cpi: 210.2,
    unemp: 7.3,
    fwd5y5y: 1.25
  },
  covid2020: {
    name: "2020 COVID-19 Deflationary Flash",
    description: "Global lockdowns trigger catastrophic employment collapse to 14.7%, WTI crude plunges, emergency Fed easing to zero.",
    oil: 18.2,
    yield10: 0.68,
    fedfunds: 0.05,
    dollar: 100.4,
    cpi: 256.4,
    unemp: 14.7,
    fwd5y5y: 1.48
  },
  normal2026: {
    name: "2024–2026 Macro Normalization",
    description: "Soft landing trajectory: Fed funds at neutral restrictive levels, energy markets balanced, long-term expectations anchored near 2.2%.",
    oil: 76.5,
    yield10: 4.15,
    fedfunds: 4.65,
    dollar: 102.8,
    cpi: 314.2,
    unemp: 4.1,
    fwd5y5y: 2.26
  }
};

class InflationSimulator {
  constructor() {
    this.inputs = {
      oil: 76.5,
      yield10: 4.15,
      fedfunds: 4.65,
      dollar: 102.8,
      cpi: 314.2,
      unemp: 4.1,
      fwd5y5y: 2.26
    };
    this.metaWeights = { xgb: 0.442, ridge: 0.558 };
  }

  // Linear Ridge baseline estimate
  predictRidge(data) {
    // Normalization factors based on historical dataset distributions
    const normFwd = (data.fwd5y5y - 2.15) / 0.35;
    const normYield = (data.yield10 - 2.80) / 1.10;
    const normOil = (data.oil - 70.0) / 25.0;
    const normDollar = (data.dollar - 98.0) / 12.0;
    const normFed = (data.fedfunds - 1.60) / 1.80;
    const normUnemp = (data.unemp - 5.50) / 1.90;

    // Ridge linear equation derived from empirical coefficient vectors
    let base = 2.18;
    base += 0.31 * normFwd;
    base += 0.12 * normYield;
    base += 0.06 * normOil;
    base -= 0.05 * normDollar;
    base -= 0.04 * normFed;
    base -= 0.03 * normUnemp;

    return Math.max(0.1, Number(base.toFixed(3)));
  }

  // Nonlinear XGBoost tree ensemble estimate
  predictXGBoost(data) {
    let ridgeVal = this.predictRidge(data);
    let nonlinearAdjustment = 0;

    // Oil shock threshold effect (piecewise nonlinearity observed in trees)
    if (data.oil > 95) {
      nonlinearAdjustment += 0.14 * Math.log(data.oil / 95);
    } else if (data.oil < 40) {
      nonlinearAdjustment -= 0.18 * (1 - data.oil / 40);
    }

    // Fed tightening regime interaction
    if (data.fedfunds > 4.5 && data.yield10 < data.fedfunds) {
      // Inverted yield curve recessionary friction
      nonlinearAdjustment -= 0.08;
    }

    // High inflation anchoring friction (5Y-5Y forward persistence)
    if (data.fwd5y5y > 2.5) {
      nonlinearAdjustment += 0.10 * (data.fwd5y5y - 2.5);
    }

    // Labor market tightness Phillips curve non-linearity
    if (data.unemp < 4.0) {
      nonlinearAdjustment += 0.05 * (4.0 - data.unemp);
    }

    const xgbVal = ridgeVal + nonlinearAdjustment;
    return Math.max(0.1, Number(xgbVal.toFixed(3)));
  }

  // Second-Stage Meta-Learner Stacked Forecast
  predictHybridStack(data) {
    const fXGB = this.predictXGBoost(data);
    const fRidge = this.predictRidge(data);

    // Meta-Ridge combining out-of-fold predictions
    const hybridVal = this.metaWeights.xgb * fXGB + this.metaWeights.ridge * fRidge;
    return {
      hybrid: Math.max(0.08, Number(hybridVal.toFixed(3))),
      xgb: fXGB,
      ridge: fRidge,
      delta: Number((hybridVal - fRidge).toFixed(3))
    };
  }

  getRegime(forecast) {
    if (forecast >= 2.65) {
      return {
        label: "Elevated Inflation Pressure",
        badgeClass: "badge-danger",
        description: "Breakeven rate is significantly elevated above the Federal Reserve's 2.0% implicit target. Financial markets price in persistent inflation risk premia."
      };
    } else if (forecast >= 2.05) {
      return {
        label: "Anchored Near Fed Target",
        badgeClass: "badge-success",
        description: "Market-based inflation expectations align closely with the Fed's 2.0% long-term target, reflecting high central bank policy credibility."
      };
    } else if (forecast >= 1.65) {
      return {
        label: "Mild Disinflationary Drag",
        badgeClass: "badge-warning",
        description: "Expectations are subdued below optimal inflation goals, typical of secular stagnation periods or restrictive liquidity conditions."
      };
    } else {
      return {
        label: "Severe Deflationary Hazard",
        badgeClass: "badge-purple",
        description: "Expectations indicate serious macroeconomic contraction or acute liquidity flight into safety (similar to late 2008 or March 2020)."
      };
    }
  }
}
