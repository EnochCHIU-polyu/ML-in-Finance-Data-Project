# Machine Learning Finance Project - S&P 500 Stock Analysis

## 📋 Project Overview

This project implements four comprehensive machine learning approaches for analyzing S&P 500 stock market data. Each notebook focuses on a different ML strategy with practical financial applications.

---

## 📊 Project Structure

```
project_folder/
├── 01_Stock_Trend_Classification.ipynb      (Classification)
├── 02_Stock_Price_Regression.ipynb          (Regression)
├── 03_Stock_Clustering_Analysis.ipynb       (Clustering)
├── 04_Anomaly_Detection.ipynb               (Anomaly Detection)
└── README.md                                (This file)
```

---

## 🎯 Four ML Approaches

### **1. Classification: Stock Trend Prediction** 📈
**File:** `01_Stock_Trend_Classification.ipynb`

**Objective:** Predict whether stock price will rise (↑) or fall (↓) next day

**Models Implemented:**
- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Support Vector Machine (SVM)

**Features:** 18 technical indicators
- Moving Averages (5, 20, 50-day)
- Relative Strength Index (RSI)
- MACD indicator
- Bollinger Bands
- Volatility metrics
- Volume analysis

**Outputs:** 6+ visualizations including:
- Model comparison metrics
- Confusion matrices
- ROC curves with AUC scores
- Feature importance analysis

**Trading Application:** 
- Generates buy/sell signals
- Best for short-term trading
- Accuracy-based position sizing

---

### **2. Regression: Price Value Prediction** 💰
**File:** `02_Stock_Price_Regression.ipynb`

**Objective:** Predict exact next day stock price value

**Models Implemented:**
- Linear Regression
- Decision Tree Regressor
- XGBoost Regressor
- Neural Network (TensorFlow)

**Evaluation Metrics:**
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- R² Score

**Outputs:** 7+ visualizations including:
- Actual vs Predicted scatter plots
- Residual analysis
- Feature importance rankings
- Neural network training history

**Trading Application:**
- Profit target placement
- Price level support/resistance
- Risk quantification via RMSE
- Confidence intervals

---

### **3. Clustering: Stock Grouping Analysis** 🎯
**File:** `03_Stock_Clustering_Analysis.ipynb`

**Objective:** Group 500 stocks into clusters based on financial characteristics

**Clustering Methods:**
- K-Means (with Elbow Method optimization)
- Hierarchical Clustering
- Cluster quality metrics (Silhouette, Davies-Bouldin)

**Grouping Features:**
- Volatility patterns
- Returns characteristics
- Trading volume
- Price momentum
- Risk profiles

**Outputs:** 5+ visualizations including:
- Optimal K selection curves
- Dendrogram (hierarchical clustering)
- 2D cluster visualization (PCA projection)
- Cluster characteristics

**Portfolio Application:**
- Portfolio diversification strategy
- Risk-balanced allocation
- Stock screening by cluster
- Cluster-based rebalancing

---

### **4. Anomaly Detection: Trading Pattern Detection** 🚨
**File:** `04_Anomaly_Detection.ipynb`

**Objective:** Detect unusual trading patterns and price anomalies

**Detection Methods:**
- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM
- Z-Score based detection
- Consensus approach (ensemble)

**Anomaly Features:**
- Extreme price movements
- Unusual volume spikes
- Return outliers
- Intraday range anomalies

**Outputs:** 5+ visualizations including:
- Anomaly score distributions
- Method comparison
- Time series with anomalies highlighted
- Feature importance for anomalies
- Stock-wise anomaly rates

**Risk Management Application:**
- Early warning system
- Position sizing adjustments
- Stop-loss triggers
- Event detection

---

## 🚀 Getting Started

### Prerequisites
```
Python 3.12
Jupyter Kernel: py312
GPU Support: NVIDIA RTX 3070 (optional but recommended)
```

### Required Packages
```
numpy, pandas, matplotlib, seaborn
scikit-learn, xgboost, tensorflow
kagglehub
```

### Installation
Packages auto-install in each notebook via `%pip install` magic command

### Data Source
- **Dataset:** S&P 500 Stock Market Data
- **Source:** Kaggle (via kagglehub)
- **Stocks Used:** Full dataset, top 5 for detailed analysis (AAPL, MSFT, GOOGL, AMZN, TSLA)

---

## 📈 Key Features

### Feature Engineering (Shared Across Models)
1. **Price Features**
   - Daily returns, price ranges, momentum indicators
   - Moving averages (5, 20, 50-day)

2. **Technical Indicators**
   - RSI (Relative Strength Index)
   - MACD-like exponential moving average
   - Bollinger Bands

3. **Volume Metrics**
   - Volume ratios, momentum
   - Abnormal volume detection

4. **Volatility Measures**
   - Rolling standard deviation
   - Intraday range analysis

### Model Comparison Framework
- Standardized evaluation metrics
- Cross-validation (5-fold)
- Performance visualization
- Best model identification

### Financial Analysis
- Trading simulation
- Risk quantification
- Portfolio implications
- Actionable recommendations

---

## 💡 Trading Strategy Integration

### Classification Model Usage
```
1. Generate daily signals (BUY/SELL)
2. Combine with technical analysis
3. Risk management: Position size based on confidence
4. Best for: Day trading, swing trading
5. Stop-loss: 2-3% below entry
```

### Regression Model Usage
```
1. Calculate predicted price targets
2. Set profit targets at predicted levels
3. Use prediction bands (±RMSE) as support/resistance
4. Risk management: Expected error quantification
5. Best for: Position trading, swing trading
```

### Clustering for Portfolio
```
1. Select representatives from each cluster
2. Allocate capital by risk profile
3. Low-volatility clusters: Core holdings (50-70%)
4. High-volatility clusters: Growth positions (10-20%)
5. Rebalance quarterly as clusters shift
```

### Anomaly Detection
```
1. Monitor daily anomaly scores
2. Alert levels: Green → Yellow → Orange → Red
3. Adjust position sizes on alerts
4. Exit positions at Red level
5. Use as risk management overlay
```

---

## 📊 Outputs Generated

Each notebook generates professional visualizations saved as PNG files:

### Classification
- `01_target_distribution.png` - Class balance
- `02_feature_correlation.png` - Feature relationships
- `03_model_comparison.png` - Metrics comparison
- `04_confusion_matrices.png` - Model accuracy details
- `05_roc_curves.png` - ROC analysis
- `06_feature_importance.png` - Important features

### Regression
- `01_price_distributions.png` - Price ranges by stock
- `02_feature_correlation_regression.png` - Feature correlation
- `03_regression_metrics_comparison.png` - Model performance
- `04_actual_vs_predicted.png` - Prediction accuracy
- `05_residual_analysis.png` - Error distribution
- `06_feature_importance_regression.png` - Feature ranks
- `07_nn_training_history.png` - Neural network learning

### Clustering
- `01_optimal_k_selection.png` - K optimization metrics
- `02_hierarchical_dendrogram.png` - Cluster hierarchy
- `03_cluster_visualization.png` - 2D cluster view
- `04_cluster_feature_distributions.png` - Feature analysis
- `05_cluster_size_distribution.png` - Cluster composition

### Anomaly Detection
- `01_anomaly_score_distributions.png` - Method scores
- `02_anomaly_detection_comparison.png` - Methods comparison
- `03_aapl_timeseries_anomalies.png` - Time series visualization
- `04_anomaly_feature_analysis.png` - Feature importance
- `05_anomaly_by_stock.png` - Stock-wise anomaly rates

---

## ⚙️ Configuration & Parameters

### Top 5 Stocks (Used for Detailed Analysis)
```
AAPL (Apple), MSFT (Microsoft), GOOGL (Google)
AMZN (Amazon), TSLA (Tesla)
```

### Key Parameters
```
Training ratio: 80/20 split
Cross-validation: 5-fold
Feature scaling: StandardScaler
Contamination rate (outliers): 5%
Neural network: 64→32→16→1 layers
```

---

## 🎓 Learning Outcomes

### Skills Demonstrated
- ✅ Machine Learning: Classification, Regression, Clustering, Anomaly Detection
- ✅ Financial Data Analysis: OHLCV data, technical indicators
- ✅ Feature Engineering: 18-25 hand-crafted indicators
- ✅ Model Evaluation: Multiple metrics, cross-validation
- ✅ Data Visualization: Professional matplotlib/seaborn plots
- ✅ Ensemble Methods: Combined predictions, consensus scoring
- ✅ GPU Acceleration: TensorFlow with CUDA support

### Practical Applications
- Trading signal generation
- Risk management systems
- Portfolio construction
- Stock screening
- Market anomaly detection

---

## 🔧 Troubleshooting

### Kernel Issues
```
If py312 kernel not found:
1. python -m jupyter kernelspec list
2. python -m ipykernel install --user --name py312 --display-name "Python 3.12"
```

### Package Installation Fails
```
Run in terminal:
pip install -r requirements.txt
Or in notebook:
%pip install --upgrade package_name
```

### Memory Issues
```
Reduce dataset: Filter to fewer stocks
Reduce batch size in neural network
Use GPU: TensorFlow auto-detects CUDA
```

### Kaggle Access
```
Place credentials at: ~/.kaggle/kaggle.json
File format: {"username":"YOUR_USER","key":"YOUR_KEY"}
```

---

## 📚 References & Resources

- **Scikit-learn:** https://scikit-learn.org
- **XGBoost:** https://xgboost.readthedocs.io
- **TensorFlow:** https://tensorflow.org
- **Kaggle Datasets:** https://kaggle.com/datasets

---

## 👤 Project Information

**Environment:**
- OS: Windows
- Python: 3.12.13
- Hardware: NVIDIA RTX 3070
- Framework: TensorFlow 2.x with CUDA support

**Data:**
- Source: Kaggle S&P 500
- Records: 1,000,000+ price points
- Stocks: 500+
- Date Range: Full historical data

---

## 📝 Next Steps

1. **Run Classification Notebook**
   - Start with 01_Stock_Trend_Classification.ipynb
   - Review generated visualizations
   - Understand model comparison metrics

2. **Execute Regression Notebook**
   - Run 02_Stock_Price_Regression.ipynb
   - Compare actual vs predicted prices
   - Analyze residual patterns

3. **Analyze Clusters**
   - Run 03_Stock_Clustering_Analysis.ipynb
   - Review cluster characteristics
   - Plan portfolio allocation

4. **Monitor Anomalies**
   - Run 04_Anomaly_Detection.ipynb
   - Identify trading day anomalies
   - Apply risk management rules

5. **Integration**
   - Combine all models for comprehensive analysis
   - Develop automated trading system
   - Implement real-time monitoring

---

**Last Updated:** [Current Date]
**Project Status:** Production-Ready ✅
