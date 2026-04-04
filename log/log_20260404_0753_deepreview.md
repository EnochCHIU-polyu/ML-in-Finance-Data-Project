# Commit Log - 20260404_0753_deepreview

- Session Time: 2026-04-04T07:53:57+08:00
- Type: Deep System Review, Report Generation & 02E Design Specification
- Author: Copilot Agent

## Session Summary

Deep review of the entire ML-in-Finance project system structure. Generated the professional full project HTML report (`PROJECT_FULL_REPORT.html`) and documented the 02E multi-horizon forecasting design specification based on the detailed technical guidance provided.

---

## Current System Results (as of 2026-04-04)

### Task 02D — ClusterNews Stacked XGBoost (Best Model)

| Model | MAE | RMSE | R² | Directional Acc | CV MAE Return |
|---|---|---|---|---|---|
| Baseline XGB | 4.6832 | 9.4606 | 0.99952 | 51.67% | 0.01212 |
| ClusterNews Direct XGB | 4.7087 | 9.4457 | 0.99952 | 51.92% | 0.01215 |
| **ClusterNews Stacked XGB** | **4.5109** | **8.8023** | **0.99958** | **54.67%** | 0.01295 |

**Key insight**: The stacked architecture (news residuals on top of price baseline) beats direct news integration. The 3.0% MAE improvement is modest but directional accuracy improvement (+3.0 pp) is the more tradeable signal.

### Per-Stock Performance (Stacked Model vs Baseline)

| Stock | Baseline MAE | Stacked MAE | MAE Δ | Baseline R² | Stacked R² |
|---|---|---|---|---|---|
| AAPL | 1.4319 | **1.4027** | -2.0% | 0.9683 | **0.9701** |
| AMZN | 10.3710 | **9.9206** | -4.3% | 0.9861 | **0.9877** |
| GOOG | 8.1966 | **7.7856** | -5.0% | 0.9788 | **0.9827** |
| MSFT | 0.5932 | 0.5794 | -2.3% | **0.9882** | 0.9882 |
| NVDA | 2.8232 | 2.8664 | +1.5% | **0.9899** | 0.9898 |

**Notable**: NVDA is the one case where the stacked model is marginally worse — likely because NVDA's price movements are driven by earnings surprises and GPU supply news that require real-time data, not 10-day lagged sentiment.

### Task 02C — Sentiment-Enhanced Cluster Regression (Prior Best)

| Model | Avg MAE | Avg R² | Stock Wins |
|---|---|---|---|
| 02C Blended | 4.8383 | 0.9816 | 1 |
| 02C Global Sentiment | 4.8383 | 0.9816 | 1 |
| 02C Cluster-Specific | 5.1066 | 0.9780 | 2 |
| 02B Blended | 7.1428 | 0.9722 | 1 |

**Best per stock (02C era)**:
- AAPL → 02C_GlobalSent (MAE 1.460)
- AMZN → 02C_ClusterSpecific (MAE 10.794)
- GOOG → 02C_ClusterSpecific (MAE 8.067)
- MSFT → 02C_Blended (MAE 0.594)
- NVDA → 02C_Blended (MAE 2.920)

### Task 03 — Clustering Method Comparison

| Method | Final Score | Silhouette | Effective Clusters | Notes |
|---|---|---|---|---|
| **K-Means (03A)** | **0.5772** | 0.2496 | 2.40 | Best balance overall; 6 clusters |
| DBSCAN (03C) | 0.5500 | **0.5652** | 1.02 | High silhouette but 9.3% noise; only 2 real clusters |
| Autoencoder+KMeans (03E) | 0.5057 | 0.2249 | 2.28 | Good separation; 4 clusters |
| GMM (03D) | 0.5022 | 0.0575 | 4.79 | Soft assignments; highest R/R cluster |
| Hierarchical (03B) | 0.4595 | 0.1965 | 2.55 | Good balance; 4 clusters |
| t-SNE+KMeans (03F) | 0.4327 | 0.1880 | 1.99 | Only 2 effective clusters; poor |

**Winner: K-Means** is the correct choice for the cluster-aware regression pipeline (used in 02C/02D) due to best composite score and clean cluster boundaries.

### Task 04 — Anomaly Detection Consensus Rates

| Stock | Total Days | Consensus Anomalies | Rate |
|---|---|---|---|
| NVDA | 1,239 | 79 | **6.38%** |
| AMZN | 1,239 | 53 | 4.28% |
| MSFT | 1,239 | 31 | 2.50% |
| AAPL | 1,239 | 25 | 2.02% |
| GOOGL | 1,239 | 23 | **1.86%** |

**Interpretation**: NVDA's 6.38% rate is notably high — driven by its GPU/AI supply shock cycles. This also explains why NVDA is the hardest stock to predict in Task 02.

---

## Deep System Analysis — What Can Be Improved

### Issue 1: Lag/Decay Grid Search Plateau
The 02C lag/decay grid search returns identical MAE (4.8484) across ALL 15 parameter combinations. This indicates:
- **Root cause**: The sentiment features have low variance at this scale; the grid search evaluation period is likely too short (single window) to distinguish parameter effects.
- **Fix**: Use TimeSeriesSplit(n_splits=5) for grid evaluation instead of single train/val split. This will surface true lag sensitivity.

### Issue 2: Static Sentiment (no velocity)
Current pipeline uses lagged raw FinBERT scores. Missing: sentiment velocity (rate of change), which is the key medium-term signal.
- **Fix**: Add `sentiment_velocity_10d` = recent 5-day avg minus prior 5-day avg (lagged). See 02E design below.

### Issue 3: NVDA Model Degradation under News
NVDA uniquely degrades under the stacked model (+1.5% MAE). Root cause: NVDA's price is driven by discrete events (earnings, NVIDIA GTC announcements) that do not map to gradual sentiment trends.
- **Fix**: Add a per-stock "news responsiveness" feature that measures the historical correlation between sentiment change and price change, used as a weight multiplier in the stacked layer.

### Issue 4: Single-Horizon Prediction (T+1 only)
All current models predict next-day price (T+1). This is the hardest horizon to forecast accurately (highest noise ratio). Medium-term horizons (T+5, T+10, T+15) offer higher signal-to-noise.
- **Fix**: Build 02E multi-horizon model — see design specification below.

### Issue 5: K-Means Clustering Uses Euclidean Distance
Current K-Means on return-correlation features uses standard Euclidean distance. Financial peer networks should use **correlation distance** (1 - |corr|) which captures co-movement regardless of level.
- **Fix**: Replace K-Means with Affinity Propagation or OPTICS on correlation distance matrix, or at minimum scale features by their financial importance before K-Means.

---

## 02E Multi-Horizon Forecasting — Design Specification

Based on the technical guidance provided, the next evolution of the system is a **multi-horizon log-return predictor**:

### Target (Y): Forward Log Returns
```
fwd_logret_5d  = ln(Close[t+5]  / Close[t])
fwd_logret_10d = ln(Close[t+10] / Close[t])
fwd_logret_15d = ln(Close[t+15] / Close[t])
```
Clipped at ±30%. Log returns are stationary, additive, and comparable across stocks.

### New Features (X additions to 02C's 24 features → 32 total)
1. **dist_ema200** — distance from 200-day EMA (trend regime indicator)
2. **ema200_slope** — 20-day slope of 200-EMA (momentum direction)
3. **dist_ema50** — distance from 50-day EMA
4. **ema50_200_cross** — golden/death cross binary signal
5. **sentiment_velocity_10d** — change in sentiment narrative momentum
6. **sentiment_acceleration** — second derivative of sentiment (rate of change of velocity)
7. **adx_14** — Wilder's ADX (trend strength, not direction)
8. **dist_52wk_high** — distance from 52-week high (reversion risk)
9. **momentum_12_1** — Jegadeesh-Titman 12-1 month momentum

### Model Architecture
- `MultiOutputRegressor(XGBRegressor(...))` — direct multi-output (not recursive)
- LightGBM alternative for native multi-output
- Separate model per K-Means cluster (reuses 02C cluster assignments)
- 80/20 temporal split with +15 trading day buffer to avoid target leakage

### Evaluation Targets
| Metric | Target |
|---|---|
| T+15 Directional Hit Rate | ≥ 55% (tradeable threshold) |
| T+15 Sharpe Ratio | ≥ 1.5 (annualized) |
| MAE improvement vs random | Statistical significance p < 0.05 |

### Output Files
- `02E_multi_horizon_predictions.csv`
- `02E_model_performance.csv`
- `02E_feature_importance.csv`
- `02E_trend_features.csv`

### Why This Matters (02F Design Preview)
Combining T+1 (from 02D) and T+15 (from 02E) creates a **regime-filtered trading signal**:
- When T+15 prediction is negative, discount any bullish T+1 signal (false breakout filter)
- VIX-conditional weighting: when VIX > 25, T+15 signal becomes more reliable than T+1
- Sentiment velocity alignment: rising velocity + positive T+15 = high-confidence entry

---

## Files Changed in This Session
- `log/log_20260404_0753_deepreview.md` (this file, new)
- `project_folder/PROJECT_FULL_REPORT.html` (new — comprehensive professional report)
- `log/README.md` (updated with this log entry)

## Extra Notes
The HTML report (`PROJECT_FULL_REPORT.html`) is the primary deliverable. It includes all metric tables with real data, architecture diagrams in CSS/HTML, and a full 02E roadmap section. The report is designed for academic/professional submission.
