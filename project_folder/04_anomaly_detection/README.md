# 04 Anomaly Detection

## Goal
Detect unusual price/volume behavior and convert alerts into risk actions.

## Folder Structure
- `data/`: Scored records and anomaly summaries
- `graph/`: Anomaly diagnostics and visual outputs
- `implementation/`: Notebook implementation

## Data Files and Number Meaning

### all_scored_records.csv
Meaning:
- Full records after feature engineering
- Includes model flags and consensus vote count

Important columns:
- `if_anomaly`, `lof_anomaly`, `svm_anomaly`, `z_anomaly`: method-level anomaly flags
- `anomaly_votes`: number of methods flagging same row
- `consensus_anomaly`: whether vote threshold is met

### consensus_anomalies.csv
Meaning:
- Subset where consensus condition is met (high-confidence anomalies)

How to read:
- These are strongest candidate events for risk controls

### stock_anomaly_summary.csv
Meaning:
- Aggregated counts/rates by stock
- `consensus_rate_%` = high-confidence anomaly frequency

How to read:
- Higher rate suggests more unstable behavior profile

## Anomaly Metrics and Number Meaning
- Isolation Forest score: lower means more anomalous
- LOF score: lower means lower local density (more outlier-like)
- One-Class SVM decision score: lower means more anomalous
- Z-score thresholding: large absolute z means unusual deviation
- Consensus votes: robustness indicator against method-specific false positives

## Graph-by-Graph Meaning

### 01_anomaly_score_distributions.png
What numbers mean:
- Histograms of score distributions for IF/LOF/SVM
- Vote distribution panel shows counts for 0..4 votes

How to read:
- Tail regions correspond to strongest anomaly candidates
- Vote distribution indicates how strict consensus threshold behaves

### 02_method_comparison.png
What numbers mean:
- Bar length = count of anomalies detected by each method and consensus

How to read:
- Large method differences indicate sensitivity differences
- Consensus count is usually lower and more conservative

### 03_aapl_timeseries_anomalies.png
What numbers mean:
- Price/volume/return time series with anomaly markers

How to read:
- Marker spikes align anomalies with market events
- Useful for event-level explanation in report

### 04_stock_consensus_rate.png
What numbers mean:
- Bar height = `consensus_rate_%` per stock

How to read:
- Higher bar means more frequent high-confidence anomaly behavior

## Practical Reporting Notes
Use these numbers in report wording:
- Why consensus threshold was chosen
- Which method is most sensitive vs most conservative
- Which stock has highest consensus anomaly rate
- How anomaly alerts map to trading-risk actions

## Suggested Risk Action Levels
- 0-1 votes: normal monitoring
- 2 votes: caution, reduce position size
- 3 votes: high alert, tighten stop-loss
- 4 votes: critical alert, review/exit depending on strategy
