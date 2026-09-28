/**
 * HybridStack Research Paper Website
 * Main Interactive Application Script
 */

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initScrollProgress();
  initScrollSpy();
  initMobileNav();
  initHeroCanvas();
  initPipelineWalkthrough();
  initSimulator();
  initBenchmarkStudio();
  initXAISuite();
  initEDAGrid();
  initModalsAndLightboxes();
  initClipboardHelpers();
  setupKaTeX();
});

/* ==========================================================================
   1. Theme Management (Dark / Light)
   ========================================================================== */
function initTheme() {
  const themeToggleBtn = document.getElementById("theme-toggle-btn");
  const currentTheme = localStorage.getItem("hybridstack-theme") || 
    (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");

  document.documentElement.setAttribute("data-theme", currentTheme);
  updateThemeIcon(currentTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const activeTheme = document.documentElement.getAttribute("data-theme");
      const targetTheme = activeTheme === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", targetTheme);
      localStorage.setItem("hybridstack-theme", targetTheme);
      updateThemeIcon(targetTheme);

      // Re-render chart colors if benchmark chart exists
      if (window.benchmarkChart) {
        window.benchmarkChart.destroy();
        renderBenchmarkChart();
      }
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.getElementById("theme-icon");
  if (!icon) return;
  if (theme === "light") {
    // Show Moon icon
    icon.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>`;
  } else {
    // Show Sun icon
    icon.innerHTML = `
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    `;
  }
}

/* ==========================================================================
   2. Scroll Progress & ScrollSpy
   ========================================================================== */
function initScrollProgress() {
  const progressBar = document.getElementById("reading-progress");
  if (!progressBar) return;

  window.addEventListener("scroll", () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = totalHeight > 0 ? (window.scrollY / totalHeight) * 100 : 0;
    progressBar.style.width = `${progress}%`;
  });
}

function initScrollSpy() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");

  window.addEventListener("scroll", () => {
    let current = "";
    const scrollPos = window.scrollY + 100;

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });
}

function initMobileNav() {
  const mobileBtn = document.getElementById("mobile-menu-btn");
  const navMenu = document.getElementById("nav-menu");

  if (mobileBtn && navMenu) {
    mobileBtn.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("mobile-open");
      mobileBtn.setAttribute("aria-expanded", isOpen);
    });

    navMenu.querySelectorAll(".nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("mobile-open");
      });
    });
  }
}

/* ==========================================================================
   3. Hero Interactive Dynamic Canvas
   ========================================================================== */
function initHeroCanvas() {
  const canvas = document.getElementById("hero-forecast-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  // Adjust for DPR
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = rect.height;

  // Generate realistic smooth time-series curves
  const points = 70;
  const actualData = [];
  const hybridData = [];
  const naiveData = [];

  let currentActual = 2.15;
  for (let i = 0; i < points; i++) {
    // Macro shock simulation
    const cycle = Math.sin(i * 0.12) * 0.45;
    const shock = (i > 38 && i < 52) ? Math.sin((i - 38) * 0.22) * 0.75 : 0;
    const noise = (Math.random() - 0.5) * 0.04;
    currentActual = 2.10 + cycle + shock + noise;
    actualData.push(currentActual);

    // HybridStack: near-perfect match (R² = 0.9999)
    hybridData.push(currentActual + (Math.random() - 0.5) * 0.005);

    // Naive / single model: lagged with visible error
    naiveData.push(currentActual + Math.sin(i * 0.35) * 0.15 - 0.08);
  }

  // Draw curves
  function draw() {
    ctx.clearRect(0, 0, w, h);

    // Grid lines
    ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
    ctx.lineWidth = 1;
    for (let y = 30; y < h; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    const minVal = 1.2;
    const maxVal = 3.4;
    const getY = (val) => h - ((val - minVal) / (maxVal - minVal)) * (h - 40) - 20;
    const getX = (idx) => (idx / (points - 1)) * (w - 20) + 10;

    // Draw Naive Baseline (faint red)
    ctx.beginPath();
    ctx.strokeStyle = "rgba(244, 63, 94, 0.35)";
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    for (let i = 0; i < points; i++) {
      const x = getX(i);
      const y = getY(naiveData[i]);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw Actual Values (White / Slate)
    ctx.beginPath();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.75)";
    ctx.lineWidth = 2;
    for (let i = 0; i < points; i++) {
      const x = getX(i);
      const y = getY(actualData[i]);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw HybridStack Predictions (Glowing Emerald)
    ctx.beginPath();
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 3;
    ctx.shadowColor = "rgba(16, 185, 129, 0.5)";
    ctx.shadowBlur = 10;
    for (let i = 0; i < points; i++) {
      const x = getX(i);
      const y = getY(hybridData[i]);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Draw glowing latest pulse point
    const lastX = getX(points - 1);
    const lastY = getY(hybridData[points - 1]);
    ctx.beginPath();
    ctx.arc(lastX, lastY, 5, 0, Math.PI * 2);
    ctx.fillStyle = "#10b981";
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  draw();
  window.addEventListener("resize", () => {
    const newRect = canvas.getBoundingClientRect();
    canvas.width = newRect.width * dpr;
    canvas.height = newRect.height * dpr;
    ctx.scale(dpr, dpr);
    draw();
  });
}

/* ==========================================================================
   4. Pipeline Walkthrough Interactivity
   ========================================================================== */
const PIPELINE_DETAILS = {
  step1: {
    title: "1. Macro Ingestion & Feature Engineering",
    description: "Continuous ingestion of 9 high-frequency FRED macroeconomic indicators spanning January 2, 2006 to October 1, 2024 (6,848 daily observations). Resampled with cubic time-aware splines to harmonize mixed reporting frequencies.",
    formula: "\\mathbf{X}_t = \\left[ \\mathbf{m}_t, \\, y_{t-1}, \\dots, y_{t-5}, \\, \\mu_{7d}(y_t) \\right] \\in \\mathbb{R}^{15}",
    rationale: "Autoregressive lag features capture short-term momentum, while the 7-day rolling mean smooths market microstructure noise without inducing temporal delay."
  },
  step2: {
    title: "2. Stage 1 Base Estimators & Bayesian Optimization",
    description: "Two structurally complementary base learners: Extreme Gradient Boosting (XGBoost) for non-linear interactions and Ridge Regression for regularized linear dynamics. Hyperparameters are tuned via Gaussian Processes with Expected Improvement (EI) acquisition.",
    formula: "\\lambda_k^* = \\arg\\min_{\\lambda \\in \\mathcal{A}_k} \\mathbb{E}_{F} \\left[ \\mathcal{L}_{\\text{CV}}(\\mathcal{M}_k(\\cdot; \\lambda)) \\right]",
    rationale: "Bayesian optimization balances exploitation and exploration across a 9-dimensional parameter space for XGBoost and L2 penalty scale for Ridge, avoiding costly exhaustive grid searches."
  },
  step3: {
    title: "3. Chronological K-Fold Out-of-Fold (OOF) Stacking",
    description: "To prevent look-ahead bias and meta-learner overfitting, training data is partitioned into K non-shuffled chronological validation folds. Base learners predict only out-of-fold instances.",
    formula: "\\mathbf{Z} = \\left[ \\mathbf{z}_{\\text{XGB}}, \\; \\mathbf{z}_{\\text{Ridge}} \\right] = \\begin{bmatrix} f_{\\text{XGB}}^{(-k(i))}(\\mathbf{x}_i) & f_{\\text{Ridge}}^{(-k(i))}(\\mathbf{x}_i) \\end{bmatrix} \\in \\mathbb{R}^{N \\times 2}",
    rationale: "Guarantees zero data leakage into the second-stage meta-feature space, ensuring out-of-sample validity in non-stationary financial regimes."
  },
  step4: {
    title: "4. Stage 2 Ridge Meta-Learner Integration",
    description: "The second-stage meta-learner fits an L2-regularized Ridge regression using the out-of-fold predictions Z as regressors against the ground truth target y.",
    formula: "\\boldsymbol{\\gamma}^* = \\arg\\min_{\\boldsymbol{\\gamma}} \\left\\{ \\|\\mathbf{y} - \\mathbf{Z}\\boldsymbol{\\gamma}\\|_2^2 + \\lambda_{\\text{meta}}\\|\\boldsymbol{\\gamma}\\|_2^2 \\right\\} \\implies \\hat{y}_* = \\gamma_1^* f_{\\text{XGB}}(\\mathbf{x}_*) + \\gamma_2^* f_{\\text{Ridge}}(\\mathbf{x}_*)",
    rationale: "A lightweight Ridge meta-learner regularizes combination weights, resolving collinearity between the base predictions while dynamically rebalancing linear vs non-linear signals."
  },
  step5: {
    title: "5. Rigorous Evaluation & Tri-Method Explainability",
    description: "Comprehensive testing against 15 baselines across 7 metrics, accompanied by post-hoc transparency via SHAP (game-theoretic global attributions), LIME (local surrogates), and PDP (partial dependence).",
    formula: "\\phi_i = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|!(|F| - |S| - 1)!}{|F|!} \\left[ f(S \\cup \\{i\\}) - f(S) \\right]",
    rationale: "Ensures forecasting outputs are fully auditable and aligned with established macroeconomic theory, fulfilling central bank transparency standards."
  }
};

/* ==========================================================================
   Mathematical Rendering Helpers (KaTeX)
   ========================================================================== */
function renderMath(element, texString, isDisplay = true) {
  if (!element || !texString) return;

  // Strip wrapping delimiters if present
  let clean = texString.trim();
  if (clean.startsWith("$$") && clean.endsWith("$$")) {
    clean = clean.slice(2, -2).trim();
  } else if (clean.startsWith("\\[") && clean.endsWith("\\]")) {
    clean = clean.slice(2, -2).trim();
  } else if (clean.startsWith("\\(") && clean.endsWith("\\)")) {
    clean = clean.slice(2, -2).trim();
  } else if (clean.startsWith("$") && clean.endsWith("$")) {
    clean = clean.slice(1, -1).trim();
  }

  if (window.katex) {
    try {
      window.katex.render(clean, element, {
        displayMode: isDisplay,
        throwOnError: false
      });
      return;
    } catch (e) {
      console.warn("KaTeX direct render error:", e);
    }
  }

  // Fallback: set delimiter text and trigger auto-render
  element.textContent = isDisplay ? `$$${clean}$$` : `\\(${clean}\\)`;
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(element, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false
      });
    } catch (err) {
      console.warn("KaTeX auto-render error:", err);
    }
  }
}

function renderAllMath(root = document.body) {
  if (!root) return;
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(root, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false,
        errorColor: '#f43f5e',
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      });
    } catch (err) {
      console.warn("KaTeX auto-render error:", err);
    }
  }
}

function setupKaTeX() {
  function tryRender(attempts = 0) {
    if (window.katex) {
      renderAllMath(document.body);
      const formulaEl = document.getElementById("pipeline-detail-formula");
      if (formulaEl && PIPELINE_DETAILS.step1) {
        renderMath(formulaEl, PIPELINE_DETAILS.step1.formula, true);
      }
    } else if (attempts < 30) {
      setTimeout(() => tryRender(attempts + 1), 100);
    }
  }
  tryRender();
  window.addEventListener("load", () => renderAllMath(document.body));
}

function initPipelineWalkthrough() {
  const stepCards = document.querySelectorAll(".step-card");
  const titleEl = document.getElementById("pipeline-detail-title");
  const descEl = document.getElementById("pipeline-detail-desc");
  const formulaEl = document.getElementById("pipeline-detail-formula");
  const rationaleEl = document.getElementById("pipeline-detail-rationale");

  if (!stepCards.length || !titleEl) return;

  // Immediately render Step 1 formula on load
  if (formulaEl && PIPELINE_DETAILS.step1) {
    renderMath(formulaEl, PIPELINE_DETAILS.step1.formula, true);
  }

  stepCards.forEach((card) => {
    card.addEventListener("click", () => {
      stepCards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");

      const stepKey = card.getAttribute("data-step");
      const info = PIPELINE_DETAILS[stepKey];
      if (info) {
        titleEl.textContent = info.title;
        descEl.textContent = info.description;
        renderMath(formulaEl, info.formula, true);
        rationaleEl.textContent = info.rationale;
      }
    });
  });
}

/* ==========================================================================
   5. Interactive Inflation Simulator
   ========================================================================== */
function initSimulator() {
  const sim = new InflationSimulator();
  const sliders = {
    oil: document.getElementById("slider-oil"),
    yield10: document.getElementById("slider-yield10"),
    fedfunds: document.getElementById("slider-fedfunds"),
    dollar: document.getElementById("slider-dollar"),
    cpi: document.getElementById("slider-cpi"),
    unemp: document.getElementById("slider-unemp"),
    fwd5y5y: document.getElementById("slider-fwd5y5y")
  };

  const valBadges = {
    oil: document.getElementById("val-oil"),
    yield10: document.getElementById("val-yield10"),
    fedfunds: document.getElementById("val-fedfunds"),
    dollar: document.getElementById("val-dollar"),
    cpi: document.getElementById("val-cpi"),
    unemp: document.getElementById("val-unemp"),
    fwd5y5y: document.getElementById("val-fwd5y5y")
  };

  const mainForecastEl = document.getElementById("sim-forecast-val");
  const xgbValEl = document.getElementById("sim-xgb-val");
  const ridgeValEl = document.getElementById("sim-ridge-val");
  const gaugeNeedle = document.getElementById("gauge-needle");
  const regimeBadge = document.getElementById("sim-regime-badge");
  const regimeDesc = document.getElementById("sim-regime-desc");

  function updateSimulation() {
    const currentData = {
      oil: parseFloat(sliders.oil?.value || 75),
      yield10: parseFloat(sliders.yield10?.value || 4.2),
      fedfunds: parseFloat(sliders.fedfunds?.value || 4.5),
      dollar: parseFloat(sliders.dollar?.value || 102),
      cpi: parseFloat(sliders.cpi?.value || 310),
      unemp: parseFloat(sliders.unemp?.value || 4.1),
      fwd5y5y: parseFloat(sliders.fwd5y5y?.value || 2.25)
    };

    // Update slider badges
    if (valBadges.oil) valBadges.oil.textContent = `$${currentData.oil.toFixed(1)}`;
    if (valBadges.yield10) valBadges.yield10.textContent = `${currentData.yield10.toFixed(2)}%`;
    if (valBadges.fedfunds) valBadges.fedfunds.textContent = `${currentData.fedfunds.toFixed(2)}%`;
    if (valBadges.dollar) valBadges.dollar.textContent = `${currentData.dollar.toFixed(1)}`;
    if (valBadges.cpi) valBadges.cpi.textContent = `${currentData.cpi.toFixed(1)}`;
    if (valBadges.unemp) valBadges.unemp.textContent = `${currentData.unemp.toFixed(1)}%`;
    if (valBadges.fwd5y5y) valBadges.fwd5y5y.textContent = `${currentData.fwd5y5y.toFixed(2)}%`;

    const result = sim.predictHybridStack(currentData);
    if (mainForecastEl) mainForecastEl.textContent = `${result.hybrid.toFixed(2)}%`;
    if (xgbValEl) xgbValEl.textContent = `${result.xgb.toFixed(2)}%`;
    if (ridgeValEl) ridgeValEl.textContent = `${result.ridge.toFixed(2)}%`;

    // Rotate gauge needle: range 0.0% to 4.0% mapped to -90deg to +90deg
    if (gaugeNeedle) {
      const clamped = Math.min(Math.max(result.hybrid, 0.5), 3.5);
      const angle = ((clamped - 0.5) / 3.0) * 180 - 90;
      gaugeNeedle.setAttribute("transform", `rotate(${angle}, 100, 100)`);
    }

    // Regime metadata
    const regime = sim.getRegime(result.hybrid);
    if (regimeBadge) {
      regimeBadge.className = `badge-tag ${regime.badgeClass}`;
      regimeBadge.textContent = regime.label;
    }
    if (regimeDesc) {
      regimeDesc.textContent = regime.description;
    }
  }

  // Bind sliders
  Object.keys(sliders).forEach((key) => {
    if (sliders[key]) {
      sliders[key].addEventListener("input", updateSimulation);
    }
  });

  // Bind presets
  const presetBtns = document.querySelectorAll(".preset-btn");
  presetBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      presetBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const presetKey = btn.getAttribute("data-preset");
      const preset = SIMULATOR_PRESETS[presetKey];
      if (preset) {
        Object.keys(sliders).forEach((key) => {
          if (sliders[key] && preset[key] !== undefined) {
            sliders[key].value = preset[key];
          }
        });
        updateSimulation();
        showToast(`Loaded scenario: ${preset.name}`);
      }
    });
  });

  updateSimulation();
}

/* ==========================================================================
   6. Benchmark Studio Table & Comparison Chart
   ========================================================================== */
let currentSortColumn = "rank";
let currentSortAsc = true;
let activeCategoryFilter = "all";

function initBenchmarkStudio() {
  renderBenchmarkTable();
  initTableSorting();
  initCategoryFilters();
  renderBenchmarkChart();
}

function renderBenchmarkTable() {
  const tbody = document.getElementById("benchmark-table-body");
  if (!tbody) return;

  let filtered = [...BENCHMARK_MODELS];
  if (activeCategoryFilter !== "all") {
    filtered = filtered.filter((m) => m.category === activeCategoryFilter);
  }

  filtered.sort((a, b) => {
    let valA = a[currentSortColumn];
    let valB = b[currentSortColumn];
    if (typeof valA === "string") valA = valA.toLowerCase();
    if (typeof valB === "string") valB = valB.toLowerCase();
    return currentSortAsc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
  });

  tbody.innerHTML = filtered
    .map(
      (m) => `
    <tr class="${m.isProposed ? "row-proposed" : ""}">
      <td class="cell-rank">${m.isProposed ? "⭐" : m.rank}</td>
      <td>
        <div class="cell-model-name">
          <span>${m.name}</span>
          <span class="badge-tag ${m.isProposed ? "badge-success" : "badge-blue"}">${m.badge}</span>
        </div>
      </td>
      <td><strong>${m.mseDisplay}</strong></td>
      <td>${m.rmse.toFixed(4)}</td>
      <td>${m.mae.toFixed(4)}</td>
      <td>${m.mape.toFixed(2)}%</td>
      <td>${m.smape.toFixed(2)}%</td>
      <td>${m.mase.toFixed(4)}</td>
      <td><strong>${m.r2Display}</strong></td>
    </tr>
  `
    )
    .join("");
}

function initTableSorting() {
  const headers = document.querySelectorAll(".benchmark-table th[data-sort]");
  headers.forEach((th) => {
    th.addEventListener("click", () => {
      const col = th.getAttribute("data-sort");
      if (currentSortColumn === col) {
        currentSortAsc = !currentSortAsc;
      } else {
        currentSortColumn = col;
        currentSortAsc = true;
      }

      headers.forEach((h) => {
        h.classList.remove("sorted-asc", "sorted-desc");
      });
      th.classList.add(currentSortAsc ? "sorted-asc" : "sorted-desc");

      renderBenchmarkTable();
    });
  });
}

function initCategoryFilters() {
  const pills = document.querySelectorAll(".filter-pill[data-filter]");
  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      pills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      activeCategoryFilter = pill.getAttribute("data-filter");
      renderBenchmarkTable();
    });
  });
}

function renderBenchmarkChart() {
  const chartCanvas = document.getElementById("benchmark-radar-chart");
  if (!chartCanvas || !window.Chart) return;

  const isLight = document.documentElement.getAttribute("data-theme") === "light";
  const gridColor = isLight ? "rgba(15, 23, 42, 0.1)" : "rgba(255, 255, 255, 0.1)";
  const textColor = isLight ? "#475569" : "#94a3b8";

  // Comparison models: HybridStack, Ridge, XGBoost, CatBoost, BiLSTM
  const topModels = [
    BENCHMARK_MODELS.find((m) => m.id === "hybridstack"),
    BENCHMARK_MODELS.find((m) => m.id === "ridge"),
    BENCHMARK_MODELS.find((m) => m.id === "xgboost"),
    BENCHMARK_MODELS.find((m) => m.id === "bilstm")
  ];

  window.benchmarkChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: ["MSE (x10⁻³)", "RMSE (x10⁻²)", "MAE (x10⁻²)", "MAPE (%)", "MASE (x10⁻¹)"],
      datasets: [
        {
          label: "⭐ HybridStack",
          data: [0.0004, 0.06, 0.04, 0.029, 0.01],
          backgroundColor: "#10b981",
          borderRadius: 4
        },
        {
          label: "Ridge Regression",
          data: [0.1, 1.13, 0.67, 0.428, 0.17],
          backgroundColor: "#06b6d4",
          borderRadius: 4
        },
        {
          label: "XGBoost",
          data: [0.6, 2.45, 1.46, 0.944, 0.37],
          backgroundColor: "#6366f1",
          borderRadius: 4
        },
        {
          label: "BiLSTM Deep Learning",
          data: [3.4, 5.80, 4.95, 2.086, 4.94],
          backgroundColor: "#f43f5e",
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: { color: textColor, font: { family: "Inter", size: 12 } }
        },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleFont: { family: "Inter", weight: "bold" }
        }
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: "Inter" } }
        },
        y: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: "JetBrains Mono" } },
          title: { display: true, text: "Scaled Error (Lower is Better)", color: textColor }
        }
      }
    }
  });
}

/* ==========================================================================
   7. Explainability (XAI) Suite
   ========================================================================== */
function initXAISuite() {
  const tabBtns = document.querySelectorAll(".xai-tab-btn");
  const panels = document.querySelectorAll(".xai-content-panel");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      panels.forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      const targetPanel = document.getElementById(btn.getAttribute("data-target"));
      if (targetPanel) targetPanel.classList.add("active");
    });
  });
}

/* ==========================================================================
   8. 32-EDA Deep Dive Showcase Grid
   ========================================================================== */
function initEDAGrid() {
  const gridEl = document.getElementById("eda-grid-container");
  const searchInput = document.getElementById("eda-search-input");
  const filterPills = document.querySelectorAll(".eda-filter-pill");

  if (!gridEl || typeof EDA_DATABASE === "undefined") return;

  let currentCategory = "all";
  let searchKeyword = "";

  function renderGrid() {
    let items = [...EDA_DATABASE];

    if (currentCategory !== "all") {
      items = items.filter((item) => item.category === currentCategory);
    }

    if (searchKeyword.trim() !== "") {
      const q = searchKeyword.toLowerCase();
      items = items.filter(
        (item) =>
          item.title.toLowerCase().includes(q) ||
          item.objective.toLowerCase().includes(q) ||
          item.keyFinding.toLowerCase().includes(q)
      );
    }

    if (items.length === 0) {
      gridEl.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--text-muted);">
          No exploratory analysis matched your search filter.
        </div>
      `;
      return;
    }

    gridEl.innerHTML = items
      .map(
        (item) => `
      <div class="eda-card" data-eda-id="${item.id}">
        <div class="eda-card-top">
          <div class="eda-card-badge">${item.categoryName}</div>
          <h4 class="eda-card-title">${item.title}</h4>
          <p class="eda-card-obj">${item.objective}</p>
        </div>
        <div class="eda-card-bottom">
          <span style="font-size: 0.75rem; color: var(--text-muted);">Analysis #${item.id}</span>
          <button class="eda-view-btn" onclick="openEDAModal(${item.id})">
            <span>View Analysis</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    `
      )
      .join("");
  }

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchKeyword = e.target.value;
      renderGrid();
    });
  }

  filterPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      filterPills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      currentCategory = pill.getAttribute("data-category");
      renderGrid();
    });
  });

  renderGrid();
}

// Global modal trigger for EDA card
window.openEDAModal = function (edaId) {
  const item = EDA_DATABASE.find((d) => d.id === edaId);
  if (!item) return;

  const modalBackdrop = document.getElementById("eda-modal-backdrop");
  const modalTitle = document.getElementById("eda-modal-title");
  const modalBody = document.getElementById("eda-modal-body");

  if (!modalBackdrop || !modalTitle || !modalBody) return;

  modalTitle.textContent = `${item.title} (#${item.id})`;
  modalBody.innerHTML = `
    <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; align-items: start;">
      <div>
        <div class="xai-image-card" onclick="openLightbox('${item.image}', '${item.title}')">
          <img src="${item.image}" alt="${item.title}">
          <div class="xai-image-zoom-overlay">🔍 Click to Expand</div>
        </div>
      </div>
      <div>
        <div class="badge-tag badge-blue" style="margin-bottom: 12px;">${item.categoryName}</div>
        <h4 style="font-size: 1.15rem; color: var(--text-heading); margin-bottom: 8px;">Methodology & Formula</h4>
        <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 16px;">
          ${item.method}
        </p>

        <h4 style="font-size: 1.15rem; color: var(--text-heading); margin-bottom: 8px;">Key Economic Insight</h4>
        <div class="xai-key-finding" style="margin-top: 0; margin-bottom: 20px;">
          ${item.keyFinding}
        </div>

        <div style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--text-muted); background: var(--bg-tertiary); padding: 10px 14px; border-radius: var(--radius-sm);">
          Code: ${item.codePath}
        </div>
      </div>
    </div>
  `;

  modalBackdrop.classList.add("open");
  renderAllMath(modalBody);
};

/* ==========================================================================
   9. Modals & Lightbox Image Viewer
   ========================================================================== */
function initModalsAndLightboxes() {
  // Close any modal via backdrop or close buttons
  document.querySelectorAll(".modal-backdrop").forEach((backdrop) => {
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop || e.target.closest(".modal-close-btn")) {
        backdrop.classList.remove("open");
      }
    });
  });

  // ESC key closes modals
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-backdrop.open").forEach((b) => b.classList.remove("open"));
    }
  });
}

window.openLightbox = function (imgSrc, caption) {
  const lightbox = document.getElementById("lightbox-modal");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxCaption = document.getElementById("lightbox-caption");

  if (lightbox && lightboxImg) {
    lightboxImg.src = imgSrc;
    if (lightboxCaption) lightboxCaption.textContent = caption || "";
    lightbox.classList.add("open");
  }
};

/* ==========================================================================
   10. Clipboard & Toast Feedback Helpers
   ========================================================================== */
function initClipboardHelpers() {
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const textToCopy = btn.getAttribute("data-copy");
      navigator.clipboard.writeText(textToCopy).then(() => {
        showToast("Copied to clipboard!");
      });
    });
  });

  const copyBibtexBtn = document.getElementById("copy-bibtex-btn");
  if (copyBibtexBtn) {
    copyBibtexBtn.addEventListener("click", () => {
      const bibtexCode = document.getElementById("bibtex-code")?.innerText;
      if (bibtexCode) {
        navigator.clipboard.writeText(bibtexCode).then(() => {
          showToast("BibTeX citation copied!");
        });
      }
    });
  }
}

function showToast(message) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
