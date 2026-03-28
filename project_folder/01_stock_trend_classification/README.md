# 01 Stock Trend Classification

## Goal
Predict whether next-day stock direction is `Up (1)` or `Down (0)`.

## Folder Structure
- `data/`: Currently empty (this task mainly outputs plots and console metrics)
- `graph/`: Final figures for classification
- `implementation/`: Notebook implementation

## Model Outputs and Number Meaning
Main evaluation numbers in this task:
- Accuracy: fraction of all correct predictions
- Precision: among predicted Up, how many are truly Up
- Recall: among true Up, how many were correctly predicted
- F1-Score: harmonic balance of Precision and Recall
- ROC-AUC: ranking quality over all probability thresholds
- CV mean/std: cross-validation stability

Interpretation rules:
- Accuracy near 0.50 means close to random binary guessing
- Precision high + Recall low means conservative Up signals
- Recall high + Precision low means aggressive Up signals
- F1 is preferred when class distribution is not perfectly balanced
- ROC-AUC > 0.5 means useful signal; ~0.5 means weak signal

## Graph-by-Graph Meaning

### 01_target_distribution.png
What numbers mean:
- Bar heights = counts of class 0 (Down) and class 1 (Up)
- Pie percentages = class proportion in total samples

How to read:
- If both classes are similar, label imbalance is low
- If one class dominates, class weighting or threshold tuning is important

### 02_feature_correlation.png
What numbers mean:
- Each cell value is Pearson correlation coefficient in [-1, 1]
- Near +1: strong positive linear relationship
- Near -1: strong negative linear relationship
- Near 0: weak linear relationship

How to read:
- Large absolute correlations between features imply possible multicollinearity
- Correlation helps feature sanity-check but does not prove causality

### 03_model_comparison.png
What numbers mean:
- Bar heights are metric scores (0 to 1)
- Baseline line at 0.50 = random binary baseline

How to read:
- Prefer models with stronger F1 and ROC-AUC, not only Accuracy
- Compare consistency across all metrics, not single metric winners

### 04_confusion_matrices.png
What numbers mean:
- Top-left: true Down predicted Down (TN)
- Top-right: true Down predicted Up (FP)
- Bottom-left: true Up predicted Down (FN)
- Bottom-right: true Up predicted Up (TP)

How to read:
- FP high: too many false buy signals
- FN high: too many missed upside opportunities

### 05_roc_curves.png
What numbers mean:
- X-axis: False Positive Rate
- Y-axis: True Positive Rate
- AUC in legend: area under ROC curve

How to read:
- Curves farther above the diagonal are better
- Higher AUC means stronger discrimination across thresholds

### 06_feature_importance.png
What numbers mean:
- Importance score per feature from tree models
- Larger value means larger contribution to split decisions

How to read:
- Top features are most influential for directional decisions
- Use this to explain model behavior and guide feature refinement

## Practical Reporting Notes
Use these numbers in report wording:
- Class balance from `01_target_distribution.png`
- Overall model ranking from `03_model_comparison.png`
- Error type discussion from `04_confusion_matrices.png`
- Probability ranking quality from `05_roc_curves.png`
- Main drivers from `06_feature_importance.png`
