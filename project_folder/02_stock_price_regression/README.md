# 02 Stock Price Regression

## Goal
Predict next-day stock price as a continuous value.

## Folder Structure
- `data/`: Currently empty (this task mainly outputs plots and console metrics)
- `graph/`: Final figures for regression
- `implementation/`: Notebook implementation

## Model Outputs and Number Meaning
Main evaluation numbers in this task:
- MAE: mean absolute error in dollars
- RMSE: root mean squared error in dollars (penalizes large errors more)
- MAPE: mean absolute percentage error
- R2 score: explained variance proportion (max 1.0)

Interpretation rules:
- Lower MAE/RMSE/MAPE is better
- RMSE >> MAE suggests outliers or occasional large misses
- MAPE helps compare error across different price levels
- R2 close to 1.0 means predictions track real variation well

## Graph-by-Graph Meaning

### 01_price_distributions.png
What numbers mean:
- X-axis = price bins
- Y-axis = sample frequency

How to read:
- Wide spread indicates higher regime diversity
- Different stocks can have very different price scales

### 02_feature_correlation_regression.png
What numbers mean:
- Correlation coefficient between features
- Range [-1, 1]

How to read:
- Strong feature-feature correlations suggest redundant information
- Useful for feature pruning or regularization decisions

### 03_regression_metrics_comparison.png
What numbers mean:
- Bars compare MAE, RMSE, MAPE, R2 across models

How to read:
- Pick model with low MAE/RMSE/MAPE and high R2
- If one model has high R2 but poor MAE, inspect scale/outlier behavior

### 04_actual_vs_predicted.png
What numbers mean:
- X-axis = actual price
- Y-axis = predicted price
- Dashed 45-degree line = perfect prediction

How to read:
- Points closer to line are better
- Curvature or fan shape indicates systematic bias or heteroscedasticity

### 05_residual_analysis.png
What numbers mean:
- Residual = actual - predicted
- Vertical zero line marks unbiased center
- Histogram spread = error dispersion

How to read:
- Mean near zero is good (low bias)
- Long tails indicate occasional large forecast errors

### 06_feature_importance_regression.png
What numbers mean:
- Relative contribution score by feature in tree-based regressors

How to read:
- Top features are strongest price-level drivers
- Useful for interpretation and reducing feature set complexity

### 07_nn_training_history.png
What numbers mean:
- Loss/MAE over epochs for train and validation sets

How to read:
- Train down + validation down: healthy learning
- Train down but validation up: overfitting
- Flat both: underfitting or weak features

## Practical Reporting Notes
Use these numbers in report wording:
- Absolute error level from MAE/RMSE
- Relative error level from MAPE
- Goodness of fit from R2
- Bias and tail risk from residual distribution
