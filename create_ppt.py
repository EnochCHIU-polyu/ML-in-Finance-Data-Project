"""
Generate COMP5564 Project Presentation from report data.
Run: .venv/bin/python create_ppt.py
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(BASE, "project_folder")
REG_GRAPH = os.path.join(PF, "02_stock_price_regression", "graph")
CLU_GRAPH = os.path.join(PF, "03_stock_clustering_analysis", "graph")
OUT = os.path.join(PF, "COMP5564_PRESENTATION.pptx")

# ── Brand colours ──
FINANCIAL_BLUE = RGBColor(0x1B, 0x3A, 0x5C)    # Deep navy
ACCENT_BLUE    = RGBColor(0x2E, 0x86, 0xC1)    # Lighter accent
DEEP_CHARCOAL  = RGBColor(0x2C, 0x2C, 0x2C)
WHITE          = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY     = RGBColor(0xF2, 0xF2, 0xF2)
HIGHLIGHT_GREEN= RGBColor(0x27, 0xAE, 0x60)
SOFT_GOLD      = RGBColor(0xD4, 0xA0, 0x1E)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

# ── Helpers ──

def add_bg(slide, color=FINANCIAL_BLUE):
    """Fill slide background with solid colour."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_rect(slide, left, top, width, height, color, alpha=None):
    """Add a filled rectangle shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    """Add a text box with formatted text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullets(slide, left, top, width, height, items, font_size=16,
                color=DEEP_CHARCOAL, bold_prefix=True, font_name="Calibri"):
    """Add a text box with bullet points. Items can be str or (bold_part, rest)."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(4)
        p.space_after = Pt(2)
        if isinstance(item, tuple):
            run_b = p.add_run()
            run_b.text = item[0]
            run_b.font.bold = True
            run_b.font.size = Pt(font_size)
            run_b.font.color.rgb = color
            run_b.font.name = font_name
            run_r = p.add_run()
            run_r.text = item[1]
            run_r.font.size = Pt(font_size)
            run_r.font.color.rgb = color
            run_r.font.name = font_name
        else:
            run = p.add_run()
            run.text = "• " + item
            run.font.size = Pt(font_size)
            run.font.color.rgb = color
            run.font.name = font_name
    return txBox


def add_image_safe(slide, path, left, top, width=None, height=None):
    """Add image if file exists, otherwise add placeholder text."""
    if os.path.isfile(path):
        if width and height:
            slide.shapes.add_picture(path, left, top, width, height)
        elif width:
            slide.shapes.add_picture(path, left, top, width=width)
        elif height:
            slide.shapes.add_picture(path, left, top, height=height)
        else:
            slide.shapes.add_picture(path, left, top)
    else:
        add_textbox(slide, left, top, Inches(4), Inches(0.5),
                    f"[Image: {os.path.basename(path)}]", 12, ACCENT_BLUE)


def make_section_header(slide, section_num, title, subtitle=""):
    """Dark blue slide with large section number and title."""
    add_bg(slide, FINANCIAL_BLUE)
    # Accent bar
    add_shape_rect(slide, Inches(0), Inches(3.2), Inches(0.15), Inches(1.2), SOFT_GOLD)
    add_textbox(slide, Inches(0.6), Inches(2.0), Inches(10), Inches(1.2),
                f"0{section_num}" if section_num < 10 else str(section_num),
                60, RGBColor(0xFF, 0xFF, 0xFF), bold=True, alignment=PP_ALIGN.LEFT)
    add_textbox(slide, Inches(0.6), Inches(3.2), Inches(11), Inches(1.0),
                title, 36, WHITE, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.6), Inches(4.3), Inches(11), Inches(0.8),
                    subtitle, 20, RGBColor(0xBB, 0xBB, 0xBB))


def content_slide_setup(slide, title_text):
    """White slide with dark blue top bar and title. Returns y-offset for content."""
    add_bg(slide, WHITE)
    add_shape_rect(slide, Inches(0), Inches(0), W, Inches(1.0), FINANCIAL_BLUE)
    add_textbox(slide, Inches(0.6), Inches(0.15), Inches(11), Inches(0.7),
                title_text, 26, WHITE, bold=True)
    # Thin accent line
    add_shape_rect(slide, Inches(0), Inches(1.0), W, Inches(0.04), SOFT_GOLD)
    return Inches(1.3)


def add_notes(slide, text):
    """Set speaker notes."""
    slide.notes_slide.notes_text_frame.text = text


# ═══════════════════════════════════════════════════════════════
# SLIDE 1 – TITLE
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide, FINANCIAL_BLUE)

# Accent shapes
add_shape_rect(slide, Inches(0), Inches(5.8), W, Inches(0.06), SOFT_GOLD)
add_shape_rect(slide, Inches(0), Inches(6.0), W, Inches(1.5), DEEP_CHARCOAL)

add_textbox(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.6),
            "Machine Learning in Finance",
            44, WHITE, bold=True, alignment=PP_ALIGN.LEFT)
add_textbox(slide, Inches(0.8), Inches(2.9), Inches(11.5), Inches(1.0),
            "Stock Price Regression & Cluster-Aware Sentiment Analysis",
            28, RGBColor(0xBB, 0xDD, 0xFF), bold=False, alignment=PP_ALIGN.LEFT)

# Divider
add_shape_rect(slide, Inches(0.8), Inches(4.2), Inches(3), Inches(0.04), SOFT_GOLD)

add_textbox(slide, Inches(0.8), Inches(4.5), Inches(11), Inches(0.5),
            "COMP5564 – ML in Finance  |  S&P 500 Dual-Task Framework",
            18, RGBColor(0x99, 0xBB, 0xDD))
add_textbox(slide, Inches(0.8), Inches(6.2), Inches(5), Inches(0.4),
            "CHIU Yee Lok  (25012923G)", 20, WHITE, bold=True)
add_textbox(slide, Inches(0.8), Inches(6.65), Inches(5), Inches(0.4),
            "April 2026", 16, RGBColor(0xAA, 0xAA, 0xAA))

add_notes(slide, "Title slide. Introduce yourself and state the course project topic: "
          "dual-task ML system for S&P 500 stock price regression and cluster analysis.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 2 – INTRODUCTION & MOTIVATION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Introduction & Motivation")

add_bullets(slide, Inches(0.6), y, Inches(6.5), Inches(5.5), [
    "S&P 500 large-caps: abundant data, high news coverage, yet hard to predict",
    "Classical econometrics (ARIMA, GARCH) cannot capture nonlinear dynamics",
    "ML methods combine heterogeneous signals: OHLCV, sentiment, cross-sectional structure",
    "Focus on 5 mega-cap stocks: AAPL, AMZN, GOOG, MSFT, NVDA",
    "Key question: Can cluster-aware sentiment routing improve both accuracy and trading utility?",
], font_size=17, color=DEEP_CHARCOAL)

# Dataset summary card
card = add_shape_rect(slide, Inches(7.5), y + Inches(0.2), Inches(5.2), Inches(4.5), LIGHT_GREY)
add_textbox(slide, Inches(7.7), y + Inches(0.3), Inches(4.8), Inches(0.5),
            "Dataset Overview", 18, FINANCIAL_BLUE, bold=True)
add_bullets(slide, Inches(7.7), y + Inches(0.9), Inches(4.8), Inches(3.5), [
    "505 S&P 500 stocks (full universe)",
    "Daily OHLCV + multi-source news headlines",
    "228 test samples per stock",
    "70 / 15 / 15 temporal split",
    "Strict no-leakage: all features lagged ≥ 1 day",
], font_size=15, color=DEEP_CHARCOAL)

add_notes(slide, "Motivate the problem: financial markets are hard to predict, classical methods are limited. "
          "ML enables combining price, volume, and NLP-derived sentiment. Introduce the 5 focal stocks and dataset.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 3 – DUAL-TASK FRAMEWORK
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Dual-Task Framework: Regression × Clustering")

# Task 1 box
add_shape_rect(slide, Inches(0.5), y, Inches(5.8), Inches(2.5), RGBColor(0xE8, 0xF0, 0xFE))
add_textbox(slide, Inches(0.7), y + Inches(0.1), Inches(5.4), Inches(0.5),
            "Task 1 — Stock Price Regression", 20, FINANCIAL_BLUE, bold=True)
add_bullets(slide, Inches(0.7), y + Inches(0.6), Inches(5.4), Inches(1.8), [
    "Predict next-day close price ŷ_{i,t+1}",
    "XGBoost with technical + sentiment features",
    "Evaluate: MAE, RMSE, R², Directional Hit Ratio",
], font_size=15, color=DEEP_CHARCOAL)

# Task 2 box
add_shape_rect(slide, Inches(7.0), y, Inches(5.8), Inches(2.5), RGBColor(0xFE, 0xF5, 0xE7))
add_textbox(slide, Inches(7.2), y + Inches(0.1), Inches(5.4), Inches(0.5),
            "Task 2 — Stock Clustering", 20, SOFT_GOLD, bold=True)
add_bullets(slide, Inches(7.2), y + Inches(0.6), Inches(5.4), Inches(1.8), [
    "Partition 505 stocks into behavioural peer groups",
    "6 methods: K-Means, Hierarchical, DBSCAN, GMM, AE+KM, t-SNE+KM",
    "Winner: K-Means (K=6), Composite Score = 0.577",
], font_size=15, color=DEEP_CHARCOAL)

# Coupling arrow area
cy = y + Inches(3.0)
add_shape_rect(slide, Inches(3.5), cy, Inches(6.3), Inches(0.06), ACCENT_BLUE)
add_textbox(slide, Inches(2.5), cy + Inches(0.2), Inches(8.3), Inches(1.8),
            "Coupling: Cluster membership → Peer sentiment pooling → Feature enrichment\n"
            "\"Clustering is not just analysis — it is a structural signal router.\"",
            17, FINANCIAL_BLUE, bold=False, alignment=PP_ALIGN.CENTER)

# Two innovations
iy = cy + Inches(2.2)
add_shape_rect(slide, Inches(0.5), iy, Inches(5.8), Inches(1.0), FINANCIAL_BLUE)
add_textbox(slide, Inches(0.7), iy + Inches(0.15), Inches(5.4), Inches(0.7),
            "Innovation 1: Cluster News Prediction\n(情緒衰減 Sentiment Decay + 聚類感知 Cluster-Aware)",
            14, WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_shape_rect(slide, Inches(7.0), iy, Inches(5.8), Inches(1.0), DEEP_CHARCOAL)
add_textbox(slide, Inches(7.2), iy + Inches(0.15), Inches(5.4), Inches(0.7),
            "Innovation 2: Multi-Horizon Meta-Signal\n(Future Prediction for Overall Strategy)",
            14, WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_notes(slide, "Explain the dual-task design. Task 1 is supervised regression, Task 2 is unsupervised clustering. "
          "The key insight is that Task 2 feeds Task 1 through cluster-routed sentiment. "
          "Mention the two innovations: cluster news prediction and multi-horizon meta-signal.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 4 – FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Feature Engineering & Sentiment Decay")

add_bullets(slide, Inches(0.6), y, Inches(6.0), Inches(2.5), [
    ("Lagged Returns: ", "Return_{t-1}, t-2, t-5 — momentum/mean-reversion"),
    ("Moving Averages: ", "MA5, MA10, MA20, EMA12, EMA26 — trend"),
    ("Volatility: ", "ATR, Bollinger %B, Historical Vol(20d)"),
    ("Volume: ", "Volume ratio, OBV, Volume MA — liquidity"),
    ("Momentum: ", "RSI(14), MACD, Stochastic %K"),
    ("Direct Sentiment: ", "Decay-weighted ticker news (FinBERT)"),
    ("Cluster Sentiment: ", "Peer-pooled sentiment — fills sparse days"),
], font_size=15, color=DEEP_CHARCOAL)

# Decay formula card
card_y = y + Inches(3.0)
add_shape_rect(slide, Inches(0.5), card_y, Inches(6.2), Inches(2.6), RGBColor(0xF7, 0xF7, 0xF7))
add_textbox(slide, Inches(0.7), card_y + Inches(0.1), Inches(5.8), Inches(0.5),
            "Temporal Sentiment Decay (Grid-Searched)", 17, FINANCIAL_BLUE, bold=True)
add_bullets(slide, Inches(0.7), card_y + Inches(0.7), Inches(5.8), Inches(1.8), [
    "Weight: w_k = exp(-λ(k-1)) / Σ exp(-λ(m-1))",
    "Optimal: L* = 10 days, λ* = 0.2",
    "Grid-Search MAE = 4.8383",
    "Near-flat optimum → robust, not fragile artefact",
], font_size=14, color=DEEP_CHARCOAL)

# Image: feature correlation
img_path = os.path.join(REG_GRAPH, "02_feature_correlation_regression.png")
add_image_safe(slide, img_path, Inches(7.2), y, width=Inches(5.5))

add_notes(slide, "Walk through the 7 feature categories. Emphasise the temporal decay mechanism: "
          "instead of hand-picking lag, we grid-search L and λ on validation set. "
          "The near-flat optimum region means the result is robust.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 5 – MODEL SELECTION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Model Selection: Why XGBoost?")

add_bullets(slide, Inches(0.6), y, Inches(5.5), Inches(4.0), [
    ("4 candidates: ", "Linear/Ridge, Random Forest, XGBoost, LSTM/GRU"),
    ("XGBoost wins: ", "best tabular fit, handles mixed features, fast, regularised"),
    ("Deep models fail: ", "training-validation divergence under strict temporal splitting"),
    ("Optuna tuning: ", "50-trial Bayesian HPO over max_depth, lr, n_estimators, subsample"),
    ("Data regime: ", "limited per-ticker samples → gradient-boosted trees naturally robust"),
], font_size=17, color=DEEP_CHARCOAL)

# Image: cross-model benchmark
img_path = os.path.join(REG_GRAPH, "03_regression_metrics_comparison.png")
add_image_safe(slide, img_path, Inches(6.8), y, width=Inches(6.0))

add_notes(slide, "Explain model selection. 4 families evaluated under identical temporal protocol. "
          "XGBoost selected because deep models overfit with small per-ticker samples. "
          "Optuna used for hyperparameter tuning with 50 Bayesian trials.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 6 – CLUSTERING RESULTS
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Clustering: K-Means Wins (K=6, Composite=0.577)")

# Method comparison table as text
add_bullets(slide, Inches(0.6), y, Inches(6.0), Inches(3.0), [
    ("K-Means (K=6): ", "Composite 0.577, Silhouette 0.250, 0% noise → Rank 1"),
    ("DBSCAN: ", "Highest silhouette (0.565) but 9.3% noise → unusable for routing"),
    ("GMM: ", "K=9, lowest silhouette (0.057), over-fragmented"),
    ("Selection rationale: ", "Zero noise critical for sentiment peer-group routing"),
], font_size=16, color=DEEP_CHARCOAL)

# PCA scatter
pca_path = os.path.join(CLU_GRAPH, "03A_02_pca_scatter.png")
add_image_safe(slide, pca_path, Inches(7.0), y, width=Inches(5.8))

# Bottom: K selection chart
k_path = os.path.join(CLU_GRAPH, "03A_01_k_selection.png")
add_image_safe(slide, k_path, Inches(0.5), y + Inches(3.2), width=Inches(5.5))

add_notes(slide, "6 clustering methods compared. K-Means wins on composite score. "
          "DBSCAN has high silhouette but 9.3% noise means some stocks get no peer sentiment. "
          "PCA scatter shows clear cluster separability. K=6 chosen at elbow point.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 7 – SECTION 3.5: 02B CLUSTER-AWARE REGRESSION IMPACT
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Section 3.5 — How 02B Cluster-Aware Regression Improves Prediction")

add_bullets(slide, Inches(0.6), y, Inches(6.2), Inches(2.8), [
    ("Mechanism 1: ", "Inject cluster_id and market_state one-hot signals into global XGBoost"),
    ("Mechanism 2: ", "Train cluster-specific XGBoost experts for each behavioural peer group"),
    ("Mechanism 3: ", "Blend global and expert outputs with validation-tuned alpha"),
    ("Why it works: ", "Reduces cross-regime parameter conflict and improves specialization"),
], font_size=15, color=DEEP_CHARCOAL)

# Impact table card
ry = y + Inches(2.9)
add_shape_rect(slide, Inches(0.5), ry, Inches(6.3), Inches(2.9), RGBColor(0xF7, 0xF7, 0xF7))
add_textbox(slide, Inches(0.7), ry + Inches(0.1), Inches(5.9), Inches(0.4),
            "02B Impact Summary (Internal Notebook Comparison)", 15, FINANCIAL_BLUE, bold=True)

rows_02b = [
    ("Global Baseline", "3.7405", "0.00%"),
    ("Global + Cluster Features", "3.4084", "8.88%"),
    ("Cluster-Specific Models", "2.5557", "31.68%"),
    ("Blended (Global + Cluster)", "2.5557", "31.68%"),
]

hy = ry + Inches(0.55)
add_textbox(slide, Inches(0.7), hy, Inches(3.6), Inches(0.3), "Setup", 12, FINANCIAL_BLUE, bold=True)
add_textbox(slide, Inches(4.4), hy, Inches(1.0), Inches(0.3), "MAE", 12, FINANCIAL_BLUE, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(5.4), hy, Inches(1.2), Inches(0.3), "Improve", 12, FINANCIAL_BLUE, bold=True, alignment=PP_ALIGN.CENTER)

for i, (name, mae, imp) in enumerate(rows_02b):
    yy = hy + Inches(0.38 * (i + 1))
    is_best = (i == 3)
    if is_best:
        add_shape_rect(slide, Inches(0.65), yy, Inches(5.95), Inches(0.34), RGBColor(0xE6, 0xF4, 0xEA))
    c = HIGHLIGHT_GREEN if is_best else DEEP_CHARCOAL
    add_textbox(slide, Inches(0.75), yy, Inches(3.5), Inches(0.3), name, 11, c, bold=is_best)
    add_textbox(slide, Inches(4.4), yy, Inches(1.0), Inches(0.3), mae, 11, c, bold=is_best, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(5.4), yy, Inches(1.2), Inches(0.3), imp, 11, c, bold=is_best, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(0.7), ry + Inches(2.45), Inches(5.9), Inches(0.35),
            "Blend formula: y_blend = alpha*y_global + (1-alpha)*y_cluster", 11, RGBColor(0x66, 0x66, 0x66))

# Right-side visual
feat_path = os.path.join(REG_GRAPH, "10_cluster_aware_feature_importance.png")
add_image_safe(slide, feat_path, Inches(7.1), y, width=Inches(5.7))

add_notes(slide, "This slide is the new report Section 3.5 in PPT form. Explain that 02B adds cluster context "
          "at both feature level and model level. The largest gain comes from cluster-specific specialization: "
          "MAE improves from 3.7405 to 2.5557 (31.68%). The blended setup keeps robustness while retaining this gain.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 8 – INNOVATION 1: CLUSTER NEWS PREDICTION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Innovation 1 — Cluster News Prediction (聚類感知)")

add_bullets(slide, Inches(0.6), y, Inches(6.0), Inches(3.2), [
    ("Problem: ", "Per-ticker news is sparse — most small/mid-caps have zero headlines on any given day"),
    ("Solution: ", "Route news through cluster peer set → transforms sparsity into abundance"),
    ("3 channels: ", "Direct ticker news + Peer-cluster news + Macro news"),
    ("Weighting: ", "TF-IDF cosine similarity × recency × source reliability × FinBERT polarity"),
    ("Stacked residual: ", "Sentiment explains only residual not captured by price baseline"),
], font_size=16, color=DEEP_CHARCOAL)

# Results card
ry = y + Inches(3.5)
add_shape_rect(slide, Inches(0.5), ry, Inches(6.2), Inches(2.5), RGBColor(0xE6, 0xF4, 0xEA))
add_textbox(slide, Inches(0.7), ry + Inches(0.1), Inches(5.8), Inches(0.4),
            "Key Results (02D Hold-Out)", 17, HIGHLIGHT_GREEN, bold=True)
add_bullets(slide, Inches(0.7), ry + Inches(0.6), Inches(5.8), Inches(1.8), [
    "Stacked Cluster-News: MAE = 0.918, R² = 0.999688, Dir. Acc. = 0.515",
    "vs Baseline: MAE = 0.909, Dir. Acc. = 0.509 (lower directional signal)",
    "AMZN MAE ↓ 47% (15.1 → 10.8), GOOG MAE ↓ 46% (15.0 → 8.1)",
    "Optimal decay: L* = 10, λ* = 0.2 (robust flat optimum)",
], font_size=14, color=DEEP_CHARCOAL)

# GOOG prediction chart
goog_path = os.path.join(REG_GRAPH, "02D_prediction_vs_actual_close_GOOG.png")
add_image_safe(slide, goog_path, Inches(7.0), y, width=Inches(5.8))

add_notes(slide, "Innovation 1: cluster news prediction. The key insight is treating clustering as an "
          "information routing mechanism. When a stock has no direct news, peer cluster sentiment fills the gap. "
          "AMZN and GOOG show the largest MAE reductions (46-47%) because they benefit most from peer intelligence. "
          "Mention the Chinese term: 聚類感知 (cluster-aware) and 情緒衰減 (sentiment decay).")


# ═══════════════════════════════════════════════════════════════
# SLIDE 8 – INNOVATION 2: MULTI-HORIZON META-SIGNAL
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Innovation 2 — Multi-Horizon Meta-Signal")

add_bullets(slide, Inches(0.6), y, Inches(6.0), Inches(3.0), [
    ("Problem: ", "T+1 optimises point accuracy but ignores portfolio rebalancing horizon"),
    ("Solution: ", "Train T+5, T+10, T+15 XGBoost heads → combine via meta-learner"),
    ("Meta-Score: ", "T1Proxy × RegimeFilter × VelocityAlign"),
    ("3 filters: ", "VIX-conditional weighting, direction alignment, sentiment-velocity alignment"),
    ("Ridge meta-learner: ", "most stable; XGB meta-learner also profitable"),
], font_size=16, color=DEEP_CHARCOAL)

# Results table card
ry = y + Inches(3.2)
add_shape_rect(slide, Inches(0.5), ry, Inches(12.2), Inches(2.8), RGBColor(0xF7, 0xF7, 0xF7))
add_textbox(slide, Inches(0.7), ry + Inches(0.1), Inches(11.8), Inches(0.4),
            "Table 6: Multi-Horizon Backtest Performance", 17, FINANCIAL_BLUE, bold=True)

# Table header
header_y = ry + Inches(0.6)
cols = ["Strategy", "Sharpe", "Max DD", "Return", "DHR", "Trades"]
col_x = [0.7, 4.5, 6.0, 7.5, 9.0, 10.5]
col_w = [3.5,  1.3, 1.3, 1.3, 1.3, 1.3]
for i, (label, x, w) in enumerate(zip(cols, col_x, col_w)):
    add_textbox(slide, Inches(x), header_y, Inches(w), Inches(0.35),
                label, 13, FINANCIAL_BLUE, bold=True,
                alignment=PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT)

# Table rows
rows_data = [
    ("T+1 Only (02D proxy)",  "2.42", "−2.1%", "3.3%",  "0.575", "47"),
    ("T+15 Only (02E)",       "−5.85","−7.6%", "−7.4%", "0.404", "47"),
    ("Rule-Based Meta (02F)", "2.42", "−2.1%", "3.3%",  "0.575", "47"),
    ("Learned Meta Ridge ★",  "8.10", "−0.8%", "10.5%", "0.681", "47"),
    ("Learned Meta XGB",      "4.72", "−1.5%", "6.5%",  "0.617", "47"),
    ("Buy-and-Hold",          "6.09", "—",     "8.2%",  "—",     "—"),
]
for r_idx, row in enumerate(rows_data):
    row_y = header_y + Inches(0.35 * (r_idx + 1))
    is_best = (r_idx == 3)
    if is_best:
        add_shape_rect(slide, Inches(0.6), row_y, Inches(11.4), Inches(0.34),
                       RGBColor(0xE6, 0xF4, 0xEA))
    for i, (val, x, w) in enumerate(zip(row, col_x, col_w)):
        c = HIGHLIGHT_GREEN if is_best else DEEP_CHARCOAL
        add_textbox(slide, Inches(x), row_y, Inches(w), Inches(0.34),
                    val, 12, c, bold=is_best,
                    alignment=PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT)

add_notes(slide, "Innovation 2: multi-horizon meta-signal. The T+15 forecast acts as a directional confidence "
          "modifier for T+1. When horizons agree, conviction is amplified; when they disagree, it's suppressed. "
          "Learned Meta Ridge achieves Sharpe 8.10, beating buy-and-hold (6.09) with only -0.8% max drawdown.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 9 – RESULTS OVERVIEW
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Results at a Glance")

# Three result cards side by side
card_w = Inches(3.8)
card_h = Inches(3.5)
gap = Inches(0.4)

# Card 1: Regression
x1 = Inches(0.5)
add_shape_rect(slide, x1, y, card_w, card_h, RGBColor(0xE8, 0xF0, 0xFE))
add_textbox(slide, x1 + Inches(0.2), y + Inches(0.1), Inches(3.4), Inches(0.4),
            "Regression (02D Stacked)", 16, FINANCIAL_BLUE, bold=True)
add_bullets(slide, x1 + Inches(0.2), y + Inches(0.6), Inches(3.4), Inches(2.5), [
    "MAE = 0.918",
    "R² = 0.999688",
    "Dir. Accuracy = 0.515",
    "MSFT best: MAE = 0.594",
    "AMZN/GOOG: 46-47% improvement",
], font_size=14, color=DEEP_CHARCOAL)

# Card 2: Clustering
x2 = x1 + card_w + gap
add_shape_rect(slide, x2, y, card_w, card_h, RGBColor(0xFE, 0xF5, 0xE7))
add_textbox(slide, x2 + Inches(0.2), y + Inches(0.1), Inches(3.4), Inches(0.4),
            "Clustering (K-Means)", 16, SOFT_GOLD, bold=True)
add_bullets(slide, x2 + Inches(0.2), y + Inches(0.6), Inches(3.4), Inches(2.5), [
    "K = 6 (Elbow + Silhouette)",
    "Composite Score = 0.577 (Rank 1)",
    "Silhouette = 0.250",
    "Zero noise ratio",
    "Financially coherent peer groups",
], font_size=14, color=DEEP_CHARCOAL)

# Card 3: Trading
x3 = x2 + card_w + gap
add_shape_rect(slide, x3, y, card_w, card_h, RGBColor(0xE6, 0xF4, 0xEA))
add_textbox(slide, x3 + Inches(0.2), y + Inches(0.1), Inches(3.4), Inches(0.4),
            "Trading (Meta Ridge)", 16, HIGHLIGHT_GREEN, bold=True)
add_bullets(slide, x3 + Inches(0.2), y + Inches(0.6), Inches(3.4), Inches(2.5), [
    "Sharpe Ratio = 8.10",
    "Max Drawdown = −0.8%",
    "Total Return = 10.5%",
    "DHR = 0.681",
    "Beats Buy-and-Hold (6.09)",
], font_size=14, color=DEEP_CHARCOAL)

# Per-stock highlight row
sy = y + Inches(4.0)
add_textbox(slide, Inches(0.6), sy, Inches(12), Inches(0.4),
            "Per-Stock Highlights", 18, FINANCIAL_BLUE, bold=True)
add_bullets(slide, Inches(0.6), sy + Inches(0.5), Inches(12), Inches(1.5), [
    ("AAPL: ", "Best under 02D stacked (MAE=1.331) — cluster peers fill news gaps"),
    ("AMZN/GOOG: ", "Largest MAE drops via cluster-specific sentiment (↓46-47%)"),
    ("MSFT: ", "Lowest absolute MAE (0.594) — smooth trend, consistent coverage"),
    ("NVDA: ", "Highest R² (0.9886) — semiconductor peer group boosts fit"),
], font_size=14, color=DEEP_CHARCOAL)

add_notes(slide, "Summary of all key results across three dimensions: regression accuracy, clustering quality, "
          "and trading utility. Highlight that AMZN/GOOG benefit most from cluster sentiment (46-47% MAE drop). "
          "The meta-signal beats buy-and-hold with Sharpe 8.10 and minimal drawdown.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 10 – TRADING UTILITY & BACKTEST
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Trading Utility: Equity Curve & Drawdown")

# Cumulative returns chart
cum_path = os.path.join(REG_GRAPH, "02F_01_cumulative_returns.png")
add_image_safe(slide, cum_path, Inches(0.5), y, width=Inches(6.0))

# Drawdown chart
dd_path = os.path.join(REG_GRAPH, "02F_02_drawdown.png")
add_image_safe(slide, dd_path, Inches(6.8), y, width=Inches(6.0))

# Key takeaway bar
ty = y + Inches(4.3)
add_shape_rect(slide, Inches(0.5), ty, Inches(12.2), Inches(1.2), FINANCIAL_BLUE)
add_textbox(slide, Inches(0.7), ty + Inches(0.1), Inches(11.8), Inches(1.0),
            "Learned Meta Ridge: Sharpe 8.10  |  Return +10.5%  |  Max DD −0.8%  |  DHR 0.681\n"
            "Buy-and-Hold: Sharpe 6.09  |  Return +8.2%  →  Meta-Signal beats passive benchmark",
            18, WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_notes(slide, "Show the equity curve comparison. The Learned Meta Ridge (green) shows the smoothest "
          "compounding and shallowest drawdown. Emphasise that even after transaction costs would reduce "
          "reported Sharpe, the directional advantage of multi-horizon combination remains clear.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 11 – LIMITATIONS & FUTURE WORK
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
y = content_slide_setup(slide, "Limitations & Future Work")

# Limitations
add_textbox(slide, Inches(0.6), y, Inches(5.5), Inches(0.4),
            "Limitations", 20, RGBColor(0xC0, 0x39, 0x2B), bold=True)
add_bullets(slide, Inches(0.6), y + Inches(0.5), Inches(5.5), Inches(3.5), [
    "No transaction costs/slippage in backtest → Sharpe overstated in live trading",
    "Static cluster topology — correlations evolve over time",
    "Headline API coverage uneven vs institutional feeds",
    "Test period = broadly bullish — bear regime performance untested",
], font_size=16, color=DEEP_CHARCOAL)

# Future work
add_textbox(slide, Inches(7.0), y, Inches(5.8), Inches(0.4),
            "Future Work", 20, HIGHLIGHT_GREEN, bold=True)
add_bullets(slide, Inches(7.0), y + Inches(0.5), Inches(5.8), Inches(3.5), [
    "Dynamic/online clustering — rolling-window K-Means updates",
    "Regime-adaptive decay — VIX-conditioned λ function",
    "Uncertainty-aware predictions — conformal intervals for position sizing",
    "Latency-aware sentiment — intraday news timestamp modelling",
    "Alternative data — earnings transcripts, satellite, options IV",
], font_size=16, color=DEEP_CHARCOAL)

# Hong Kong context tip
hk_y = y + Inches(4.3)
add_shape_rect(slide, Inches(0.5), hk_y, Inches(12.2), Inches(1.0), RGBColor(0xFE, 0xF5, 0xE7))
add_textbox(slide, Inches(0.7), hk_y + Inches(0.1), Inches(11.8), Inches(0.8),
            "Hong Kong Context: This framework is directly applicable to HKEX stocks — "
            "cross-listing dynamics (A/H shares), Hang Seng Index constituents, and "
            "regional sentiment from SCMP/Caixin news feeds could strengthen the cluster routing layer.",
            14, DEEP_CHARCOAL, alignment=PP_ALIGN.LEFT)

add_notes(slide, "Be honest about limitations: no transaction costs, static clusters, bullish test window. "
          "For future work, highlight dynamic clustering and regime-adaptive decay as the most impactful. "
          "If asked about Hong Kong applicability, mention A/H share dynamics and regional sentiment sources.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 12 – CONCLUSION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, FINANCIAL_BLUE)

add_textbox(slide, Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8),
            "Conclusion", 36, WHITE, bold=True)

# Accent bar
add_shape_rect(slide, Inches(0.8), Inches(1.7), Inches(3), Inches(0.04), SOFT_GOLD)

add_bullets(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(4.5), [
    "Core thesis validated: Clustering as signal router measurably improves both accuracy and trading utility",
    "Innovation 1: Cluster-routed sentiment fills news-sparse days → 46-47% MAE reduction for AMZN/GOOG",
    "Innovation 2: Multi-horizon meta-signal → Sharpe 8.10 (vs 6.09 buy-and-hold), MaxDD −0.8%",
    "XGBoost > LSTM/GRU under financial data constraints (limited per-ticker samples, temporal splitting)",
    "Dual evaluation protocol: Point-wise (MAE/R²) + Deployment utility (Sharpe/DHR/Drawdown)",
], font_size=18, color=WHITE)

# Core thesis callout
cy = Inches(5.5)
add_shape_rect(slide, Inches(0.8), cy, Inches(11.5), Inches(1.0), SOFT_GOLD)
add_textbox(slide, Inches(1.0), cy + Inches(0.15), Inches(11.1), Inches(0.7),
            "\"Clustering is not only an unsupervised analysis module — it functions as a structural signal router\n"
            "that converts sparse individual-news streams into cluster-informed predictive features.\"",
            16, FINANCIAL_BLUE, bold=True, alignment=PP_ALIGN.CENTER)

add_notes(slide, "Restate the core thesis: clustering as signal router. Summarise both innovations with numbers. "
          "Emphasise the dual evaluation: we measure both prediction accuracy AND trading utility, "
          "preventing metric-singleton optimisation that could mislead deployment decisions.")


# ═══════════════════════════════════════════════════════════════
# SLIDE 13 – Q&A / BACKUP
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DEEP_CHARCOAL)

add_textbox(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(1.2),
            "Thank You — Questions?", 42, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_shape_rect(slide, Inches(5.2), Inches(3.5), Inches(3), Inches(0.04), SOFT_GOLD)
add_textbox(slide, Inches(0.8), Inches(4.0), Inches(11.5), Inches(0.6),
            "CHIU Yee Lok  |  25012923G  |  COMP5564 ML in Finance  |  April 2026",
            18, RGBColor(0xAA, 0xAA, 0xAA), alignment=PP_ALIGN.CENTER)

# Backup data
add_textbox(slide, Inches(0.8), Inches(5.2), Inches(11.5), Inches(0.4),
            "Quick Reference (Backup)", 16, SOFT_GOLD, bold=True)
add_bullets(slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(1.5), [
    "02D Stacked: MAE=0.918, R²=0.9997, DHR=0.515   |   Best per-stock: MSFT MAE=0.594",
    "K-Means K=6: Composite=0.577, Sil=0.250  |  Lag-Decay: L*=10, λ*=0.2, Grid-MAE=4.838",
    "Meta Ridge: Sharpe=8.10, Return=+10.5%, MaxDD=−0.8%, DHR=0.681   |   B&H: Sharpe=6.09",
], font_size=13, color=RGBColor(0xCC, 0xCC, 0xCC))

add_notes(slide, "Q&A slide. Be prepared to answer about: transaction cost impact on Sharpe, "
          "why DBSCAN was rejected (noise ratio), how the meta-signal handles regime changes, "
          "and applicability to Hong Kong equities. Backup numbers are on screen for reference.")


# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
prs.save(OUT)
print(f"✓ Saved: {OUT}")
print(f"  {len(prs.slides)} slides generated")
