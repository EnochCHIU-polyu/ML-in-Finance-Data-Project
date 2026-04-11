# Institutional Remediation Changelog
**Date:** April 2026  
**Scope:** Full project_folder remediation pass  

## Summary of Changes

### All Three Reports (QIS_ALPHA_REPORT.html, COMP5564_report_real.html, QIS_ALPHA_REPORT copy.html)

#### 1. Factual Correction: WFO Window Count
- **Was:** "13 expanding windows × 15-day OOS slices = 195 OOS trading days"
- **Corrected to:** "5 expanding windows × 20-day OOS = 100 OOS trading days"
- **Evidence:** `02F_walkforward_oos.csv` contains exactly 5 windows (2017-08-04 to 2017-12-26)
- **Why changed:** The previous claim was factually wrong and inflated the robustness of the OOS validation

#### 2. Corrected Strategy Backtest Metrics (Table 4)
- **Was:** T+1 Sharpe=2.42, Ridge Sharpe=3.91, XGB Sharpe=4.45 (source unclear)
- **Corrected to:** T+1=0.86, Ridge=2.85, XGB=2.19 (source: `02F_backtest_performance.csv`, 5bps one-way cost)
- **Also added:** OOS days per strategy (46 for T+1/T+15/Rule-Based/Ridge; 99 for XGB) and BH Sharpe per window
- **Why changed:** Previous values were from an untracked older run; current CSV values are authoritative

#### 3. WFO Summary Table (Table 4A) Updated
- **Was:** Estimated win-rates based on 13-window claim (~69% for XGB, ~30% for T+1)
- **Corrected to:** Computed directly from CSV: XGB 4/5=80%, T+1/Rule-Based/Ridge 2/5=40%, BH 4/5=80%, Mean Sharpe values added
- **Why changed:** Win-rates must be traceable to actual data rows

#### 4. R² Explanation Added (Section 4.1)
- **Added:** Callout explaining that near-1.0 R² on price levels is expected (autocorrelation artifact) and is NOT a signal quality metric
- **Financially relevant metrics:** Directional accuracy (~51%) and CV MAE on returns
- **Why added:** Without this explanation, R²≈0.9997 appears to be a leakage indicator or trivial problem

#### 5. Net-Cost Stress Table Added (Section 5.4 / Table 5A)
- **Added:** Quantitative table with 3 institutional cost scenarios from `02F_stress_test_robust_wfo.csv`
  - 5bps/20% ADV: Sharpe −4.11 [CI: −7.15, −1.25], IR −5.09 → FAIL
  - 10bps/10% ADV: Sharpe −3.87 [CI: −7.04, −1.05], IR −4.86 → FAIL  
  - 20bps/5% ADV: Sharpe −2.97 [CI: −6.48, −0.13], IR −4.31 → FAIL
- **Why added:** Previously "Partial" or conceptual; now provides evidence-based cost stress results

#### 6. Reproducibility Manifest Updated (Section 6.6 / Table 6A)
- **Was:** All items marked "Missing"
- **Updated to:** Partial values with actual content:
  - OOS timestamps: Present (WFO: 2017-08-04 to 2017-12-26)
  - Random seeds: Partial (XGBoost=42, KMeans=42 — full list not consolidated)
  - Parameters: Partial (in notebooks; not exported to standalone file)
  - Data sources: Partial (named; file hashes missing)
  - Requirements.txt and git SHA: still Missing
- **Why changed:** "Missing" for all items was factually inaccurate; actual partial evidence exists

#### 7. Final Pass/Fail Checklist and Explicit FAIL Status Added (Section 7)
- **Added:** Section 7.1 with explicit pass/fail table for all 13 institutional criteria
- **Final status:** ❌ FAIL explicitly stated with 5 specific reasons
- **Why added:** Reports previously used vague language ("not yet sufficient"); institutional reviewers require an explicit binary decision

#### 8. Executive Summary Updated
- All three reports updated to use actual CSV Sharpe values and to note the FAIL conclusion
- Promotional language removed; replaced with evidence-proportionate wording

### COMP5564_report_real.html — Additional Changes

#### 9. Reviewer Memo Updated to Show Resolution Status
- Each blocker item marked as: ✓ ADDRESSED, ✗ OPEN, or ⚠ PARTIALLY ADDRESSED
- Pass/fail checklist updated from unchecked boxes to actual status indicators
- Decision rule updated to reflect FAIL with specific unresolved items

### QIS_ALPHA_REPORT copy.html — Additional Changes

#### 10. Section 5.4 Added (Net-Cost Stress)
- The copy was missing Section 5.4 entirely; added Table 5A with the 3 cost scenarios

## What Was NOT Changed (and Why)

- **Notebook cells were not re-run:** The data in CSVs is authoritative; re-running would require the full Python environment
- **Figures were not regenerated:** WFO figure captions updated to note 5 windows; actual PNG files not changed (figure already reflects current data)
- **02D Table 3 values:** Already correct from CSV (R²≈0.9997 values retained with explanation note)
- **IC/ICIR Table 4B values:** Values from `02F_cross_sectional_ic.csv` appear consistent; retained with note about 47-day window limitation

## Open Items Requiring Future Work

1. **Nested validation:** Implement proper inner/outer split in 02F pipeline
2. **Factor-neutral benchmark:** Add Fama-French or industry factor comparison
3. **Subperiod analysis:** Add bull/bear, pre/post volatility tables
4. **Robustness checks:** Shuffled-label placebo, seed sensitivity, k-cluster variants
5. **Full reproducibility:** Export requirements.txt, file hashes (SHA-256), git commit SHA
6. **Slippage/impact model:** Move from conceptual to empirical calibration
