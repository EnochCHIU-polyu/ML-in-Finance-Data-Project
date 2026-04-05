# 02E Multi-Horizon Forecasting — v2 Optimizations

**Update Date:** 2026-04-05  
**Objective:** Address 4 high-impact performance bottlenecks identified in preliminary diagnostics.

---

## 1. Carry-Forward + Coverage Gating for Sentiment Signals

### Problem

- Original 02D sentiment output had **8–13% non-zero coverage**, causing sentiment features to be almost silent.
- Many trading days had zero sentiment despite the prior day having meaningful news.
- Stocks with sparse news coverage added noise rather than signal.

### Solution

**Implemented in 02E Step 2 (Sentiment Loading):**

```python
# Carry-forward: Fill zero-sentiment days with decayed previous signal
apply_carry_forward(group, lookback_days=3, decay_factor=0.85)
# Example: If news sentiment was +0.15 yesterday (and 0 today), today gets +0.15 * 0.85 = +0.1275

# Coverage gating: Stocks with sparse news coverage → sentiment weighted down
coverage_threshold = 0.05  # Require 5% of days with non-zero coverage
coverage_gate = where(coverage >= threshold, 1.0, coverage / threshold)
raw_sentiment *= coverage_gate
```

**Expected Impact:**

- Non-zero sentiment rows: 8–13% → **40–50%+** (with carry-forward)
- Sentiment feature importance: ~0% → **3–5%+** (unblocked signal)
- DHR boost: Particularly for stocks with news momentum indicators

---

## 2. Time-Aware Dynamic Clustering

### Problem

- Original clustering used **static per-stock mode**: `cluster_assignment = df.groupby('Name')['cluster'].mode()`
- This ignored market regime changes (high-vol clusters stay isolated year-round)
- Cluster-aware training couldn't adapt to changing peer relationships

### Solution

**Implemented in 02E Step 2a (New cell after cluster assignment):**

```python
# For each date, recompute clusters based on rolling 60-day return characteristics
for date in all_dates:
    lookback_df = price_df[(price_df['date'] >= date - 60 days) & (price_df['date'] <= date)]

    # Compute return features: mean return, volatility, skewness, momentum
    features = [ret_mean, ret_vol, ret_skew, momentum]

    # Adaptive K-Means: cluster count ~ 6 (or fewer if few stocks)
    clusters[date] = KMeans(n_clusters=6).fit_predict(features)

# Result: Dynamic cluster map { date → { stock → cluster_id } }
```

**Cluster Rebalance Schedule:**

- Computed daily but can be thinned (e.g., rebalance every 20 trading days)
- When exact date not found, use nearest prior date's clusters

**Expected Impact:**

- Cluster-aware models now reflect **market microstructure changes**
- Stocks migrate from safe → risk clusters during volatility spikes
- Per-cluster models adapt naturally to regime shifts
- DHR variance across stocks should decrease by **3–8%**

---

## 3. Separate Horizon-Specific Models + Tuned Parameters

### Problem

- Original: Single `MultiOutputRegressor(XGBoost)` shared parameters across T+5, T+10, T+15
- Longer horizons were over-regularized (conservative to avoid T+5 overfitting)
- Short-term predicting was under-regularized (could capture T+5 noise)
- Results: T+5 weak, T+15 weaker

### Solution

**Implemented in 02E Step 3a and 4:**

```python
# Define per-horizon parameters
XGB_PARAMS_BY_HORIZON = {
    5:  { max_depth: 5,  min_child_weight: 3, subsample: 0.90 },  # Aggressive
    10: { max_depth: 6,  min_child_weight: 4, subsample: 0.87 },  # Moderate
    15: { max_depth: 7,  min_child_weight: 6, subsample: 0.83 },  # Conservative
}

# Train three separate XGBRegressor models
for h in [5, 10, 15]:
    models_by_horizon[h] = XGBRegressor(**XGB_PARAMS_BY_HORIZON[h])
    models_by_horizon[h].fit(X_train, y_train[f'fwd_logret_{h}d'])
    preds_by_horizon[h] = models_by_horizon[h].predict(X_test)
```

**Per-Horizon Tuning Rationale:**

- **T+5 (short-term):** More aggressive (shallower, less min_child_weight) to capture tactical reversals
- **T+10 (medium):** Balanced regularization
- **T+15 (long-term):** Deeper trees with high min_child_weight to prevent overfitting on macro noise

**Expected Impact:**

- T+5 DHR: 48% → **52–54%** (capture mean-reversion better)
- T+10 DHR: 48% → **49–51%** (slight improvement)
- T+15 DHR: 49% → **51–55%** (reduce overfitting, increase calibration)
- Per-stock variance: Should stabilize (less models fighting each other)

---

## 4. Walk-Forward Validation Framework

### Problem

- Original evaluation: single 80/20 temporal split → one data point (could be lucky/unlucky)
- No insight into model stability across different market regimes
- Can't diagnose whether model breaks in certain periods

### Solution

**Implemented in 02E Step 5 (new cell):**

```python
# Define rolling windows
WF_TRAIN_WINDOW = 120 days    # ~6 months
WF_TEST_WINDOW = 60 days      # ~3 months
WF_STEP = 30 days             # Roll every month

# For each fold (e.g., Fold 1, 2, 3, ...):
for fold in folds:
    train_df = df[fold.train_start : fold.train_end]
    test_df  = df[fold.test_start : fold.test_end]

    for h in [5, 10, 15]:
        model_fold = XGBRegressor(**params_h).fit(X_train, y_train[h])
        results[fold][h] = evaluate(model_fold.predict(X_test), y_test[h])
```

**Walk-Forward Metrics Tracked:**

```
For each horizon:
  - Mean DHR across folds
  - Std DHR across folds   ← Key: low std = stable model
  - Mean R², Mean Sharpe
  - Folded results saved → 02E_walkforward_results.csv
```

**Stability Thresholds:**

- DHR std < 0.05 (5%) → ✓ Model is robust
- DHR std > 0.10 (10%) → ⚠ Model overfits to certain market regimes

**Expected Impact:**

- Identify if model degrades in volatile periods
- Detect regime-specific overfitting
- **Expected DHR stability:** ~0.03–0.05 across folds (good)
- Can trigger retraining if std > threshold

---

## Implementation Checklist

| Feature                   | Cell                   | Status | Notes                                    |
| ------------------------- | ---------------------- | ------ | ---------------------------------------- |
| Carry-forward sentiment   | #VSC-dd074dc9 (edited) | ✅     | Pre-processing during sentiment load     |
| Coverage gating           | #VSC-dd074dc9 (edited) | ✅     | Dampens sentiment for sparse-news stocks |
| Dynamic clustering        | #VSC-5f84762b (new)    | ✅     | Time-aware cluster assignment per date   |
| Per-horizon models        | #VSC-eac59ddb (edited) | ✅     | T+5/T+10/T+15 trained separately         |
| Tuned parameters          | #VSC-d19699c5 (edited) | ✅     | XGB_PARAMS_BY_HORIZON config             |
| Cluster-aware per-horizon | #VSC-0ba63ef2 (edited) | ✅     | Combines clustering + separate models    |
| Walk-forward validation   | #VSC-169ff707 (new)    | ✅     | 3 folds rolling, stability metrics       |

---

## How to Run the Updated 02E Notebook

```bash
# Ensure 02D has been run (generates 02D_cluster_news_features.csv)
cd /path/to/02_stock_price_regression/implementation

# Run 02E with new improvements
jupyter notebook 02E_Multi_Horizon_Forecasting.ipynb
# or in VS Code Jupyter: execute all cells

# Outputs:
#   - 02E_model_performance.csv          (per-stock per-horizon metrics)
#   - 02E_multi_horizon_predictions.csv  (full pred table)
#   - 02E_walkforward_results.csv        (fold-wise validation)
#   - 02E_trend_features.csv             (X/y for debugging)
#   - Plots: DHR/Sharpe distributions, reliability curves
```

---

## Expected Performance Improvements

### Conservative Estimate (3–6 months implementation)

| Metric                       | Before | After  | Improvement |
| ---------------------------- | ------ | ------ | ----------- |
| Mean DHR (T+5)               | 48.0%  | 52.0%  | +4.0 pp     |
| Mean DHR (T+10)              | 47.8%  | 49.5%  | +1.7 pp     |
| Mean DHR (T+15)              | 48.9%  | 51.5%  | +2.6 pp     |
| Sentiment feature importance | ~0%    | 3–5%   | Unblocked   |
| Stocks reaching DHR ≥55%     | 28%    | 35–40% | +7–12 pp    |
| Walk-forward DHR std         | —      | <0.05  | Stable      |

### Optimistic Estimate (if all tunings align well)

| Metric                        | Before | After  | Improvement |
| ----------------------------- | ------ | ------ | ----------- |
| Mean DHR (T+15)               | 48.9%  | 55.0%+ | +6 pp+      |
| Sharpe (T+15)                 | 0.28   | 0.50+  | +0.2 pp+    |
| Coverage (non-zero sentiment) | 10%    | 50%    | 5×          |

---

## Next Steps

1. **Execute 02E with all improvements** and monitor:
   - Are sentiment features now meaningful (importance > 2%)?
   - Do walk-forward folds have low std (<0.05)?
   - Which horizon (T+5/T+10/T+15) benefits most?

2. **If walk-forward stability is good (<0.05 std):**
   - Freeze parameters and deploy for live trading
   - Rebalance clusters monthly

3. **If walk-forward shows regime-specific weakness (e.g., std >0.10):**
   - Implement regime detection (VIX-based or Hidden Markov Model)
   - Use regime-specific model parameters

4. **Fine-tune per-horizon parameters** based on validation results:
   - If T+15 is still weak: increase max_depth or reduce min_child_weight
   - If T+5 is overfitting: increase subsample or reduce learning_rate

5. **Scale improvements to 02F (Regime Filtered Signal):**
   - 02F currently uses 02E as upstream input
   - Improved 02E predictions → better 02F regime filtering

---

## Detailed Code Changes Summary

### Sentiment Enhancement (02E Step 2)

- **Lines added:** ~80 lines
- **Key functions:** `apply_carry_forward()`, coverage gating loops
- **Config:** `COVERAGE_THRESHOLD = 0.05`, `decay_factor=0.85`

### Dynamic Clustering (02E Step 2a – NEW)

- **Lines added:** ~50 lines
- **Key function:** `get_daily_cluster()` for lookup
- **Config:** `CLUSTER_REBALANCE_DAYS = 20`, lookback window = 60 days

### Per-Horizon Models (02E Step 3a + 4)

- **Lines changed:** ~40 lines (replaced MultiOutputRegressor logic)
- **New config:** `XGB_PARAMS_BY_HORIZON` dict with 3 entries
- **Key change:** Loop over `HORIZONS` instead of single model

### Walk-Forward Validation (02E Step 5 – NEW)

- **Lines added:** ~100 lines
- **Config:** `WF_TRAIN_WINDOW=120`, `WF_TEST_WINDOW=60`, `WF_STEP=30`
- **Output:** `02E_walkforward_results.csv` with fold-wise metrics

---

## References

- **Carry-forward & gating:** Industry-standard in time-series ML (addresses missing data)
- **Dynamic clustering:** Similar to rolling factor models (adapts to market regimes)
- **Per-horizon tuning:** Standard in multi-step forecasting (different horizons have different risk profiles)
- **Walk-forward validation:** Industry best practice (avoids overfitting bias from single splits)

---

**Document generated:** 2026-04-05  
**Notebook updated:** 02E_Multi_Horizon_Forecasting.ipynb  
**Total changes:** 270+ lines (implementations + configs)
