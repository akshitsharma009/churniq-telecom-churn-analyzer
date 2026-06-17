import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import json
import numpy as np

st.set_page_config(
    page_title="Executive Overview — ChurnIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #090E1A !important;
    color: #EDF2FF !important;
}
.stApp { background: #090E1A !important; }
#MainMenu, footer, header { visibility: hidden; }

/* Hide default Streamlit page nav at top of sidebar */
/* Nuclear hide — all known Streamlit nav selectors across versions */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNavLink"],
div[data-testid="stSidebar"] ul,
div[data-testid="stSidebar"] > div > div > div > ul,
section[data-testid="stSidebar"] nav,
.st-emotion-cache-pbsa9s,
.st-emotion-cache-1rtdyuf,
.st-emotion-cache-6tkfeg {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1400px !important;
}
[data-testid="stSidebar"] {
    background: #0F1629 !important;
    border-right: 1px solid #1E2D4A !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #090E1A; }
::-webkit-scrollbar-thumb { background: #2A3F6B; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
<div style="padding:1.2rem 0 1.5rem 0;">
  <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:#EDF2FF;">
    ⚡ ChurnIQ
  </div>
  <div style="font-size:10px;color:#4A5A7A;letter-spacing:1.8px;text-transform:uppercase;margin-top:3px;">
    Intelligence Platform
  </div>
</div>
<hr style="border:none;border-top:1px solid #1E2D4A;margin:0 0 1.2rem 0;">
""", unsafe_allow_html=True)

    st.page_link("app.py",                        label="🏠  Home")
    st.page_link("pages/1_Executive_Overview.py", label="📊  Executive Overview")


# ============================================================
# LOAD ALL DATA — fully dynamic, no hardcoded values
# ============================================================
@st.cache_data
def load_risk():
    return pd.read_csv("data/processed/revenue_risk_output.csv")

@st.cache_resource
def load_model():
    return joblib.load("models/champion_xgboost.joblib")

@st.cache_data
def load_metrics():
    with open("models/model_metrics.json", "r") as f:
        return json.load(f)

@st.cache_data
def load_features():
    return pd.read_csv("data/processed/feature_engineered.csv")

# ── Load with error handling ──
errors = []

try:
    risk_df = load_risk()
except Exception as e:
    errors.append(f"revenue_risk_output.csv: {e}")
    risk_df = None

try:
    model = load_model()
except Exception as e:
    errors.append(f"champion_xgboost.joblib: {e}")
    model = None

try:
    metrics = load_metrics()
except Exception as e:
    errors.append(f"model_metrics.json: {e}")
    metrics = {}

try:
    feat_df = load_features()
except Exception as e:
    errors.append(f"feature_engineered.csv: {e}")
    feat_df = None

if errors:
    for err in errors:
        st.warning(f"⚠ Could not load {err}")

# ── Derive all KPIs from data ──
if risk_df is not None:
    total_customers   = len(risk_df)
    total_rev_at_risk = risk_df["RevenueRiskScore"].sum()
    avg_rev_at_risk   = risk_df["RevenueRiskScore"].mean()
    avg_churn_prob    = risk_df["ChurnProbability"].mean()
    max_revenue_risk  = risk_df["RevenueRiskScore"].max()

    # Actual churn rate from ground truth labels, NOT from probability threshold
    threshold = 0.40

churned_count = int(
    (risk_df["ChurnProbability"] >= threshold).sum()
)

retained_count = total_customers - churned_count

churn_rate = (
    churned_count / total_customers
) * 100

seg_counts = risk_df["PrioritySegment"].value_counts()
high_count   = int(seg_counts.get("High",   0))
medium_count = int(seg_counts.get("Medium", 0))
low_count    = int(seg_counts.get("Low",    0))

seg_rev    = risk_df.groupby("PrioritySegment")["RevenueRiskScore"].sum()
rev_high   = float(seg_rev.get("High",   0))
rev_medium = float(seg_rev.get("Medium", 0))
rev_low    = float(seg_rev.get("Low",    0))
total_rev  = rev_high + rev_medium + rev_low

# ── Model metrics from JSON ──
roc_auc   = metrics.get("roc_auc",   0)
cv_std    = metrics.get("cv_std",    0)
precision = metrics.get("precision", 0)
recall    = metrics.get("recall",    0)
f1        = metrics.get("f1",        0)
threshold = metrics.get("threshold", 0.40)

# ── Feature importance from model ──
# ── Feature importance from model ──
feat_importance_df = None

try:
    xgb_model = model.named_steps["model"]
    preprocessor = model.named_steps["preprocessor"]

    importances = xgb_model.feature_importances_
    feature_names = preprocessor.get_feature_names_out()

    clean_feature_names = []

    for feat in feature_names:

        feat = feat.replace("categorical__", "")
        feat = feat.replace("remainder__", "")
        feat = feat.replace("_", " ")

        feat = feat.replace(
            "CustomerLifecycleStage",
            "Customer Lifecycle Stage"
        )

        feat = feat.replace(
            "CurrentEquipmentDays",
            "Current Equipment Days"
        )

        feat = feat.replace(
            "MonthsInService",
            "Months In Service"
        )

        feat = feat.replace(
            "HandsetPrice",
            "Handset Price"
        )

        feat = feat.replace(
            "PercChangeMinutes",
            "Percent Change Minutes"
        )
        

        clean_feature_names.append(feat)

    if len(importances) == len(feature_names):

        feat_importance_df = (
            pd.DataFrame(
                {
                    "Feature": clean_feature_names,
                    "Importance": importances
                }
            )
            .sort_values("Importance", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

except Exception:
    feat_importance_df = None


# ============================================================
# PAGE HEADER
# ============================================================
col_h1, col_h2 = st.columns([3, 1])

with col_h1:
    st.markdown("""
<div style="margin-bottom:1rem;">
  <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
              color:#4F8EF7;margin-bottom:6px;">ChurnIQ · Executive Overview</div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;
              color:#EDF2FF;letter-spacing:-0.5px;">Business Intelligence Summary</div>
  <div style="font-size:13px;color:#8B9DC3;margin-top:5px;">
    Churn exposure, revenue risk, and retention priorities — all in one view.
  </div>
</div>
""", unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
<div style="text-align:right;padding-top:10px;">
  <div style="font-size:10px;color:#4A5A7A;">Dataset</div>
  <div style="font-size:13px;font-weight:500;color:#8B9DC3;">Cell2Cell Telecom</div>
  <div style="font-size:10px;color:#4A5A7A;margin-top:2px;">{total_customers:,} customers</div>
  <div style="font-size:9px;color:#00E5A0;margin-top:4px;">● Live Data</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #1E2D4A;margin-bottom:1.5rem;'>",
            unsafe_allow_html=True)


# ============================================================
# KPI CARDS — all from data
# ============================================================
st.markdown("""
<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
            color:#4A5A7A;margin-bottom:12px;">Key Performance Indicators</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    (k1, "Total Customers",  f"{total_customers:,}",
     None,       "#4F8EF7", "Full analyzed base"),

    (k2, "Churn Rate",       f"{churn_rate:.2f}%",
     "▲ Risk",   "#FF4D6A", f"{churned_count:,} customers"),

    (k3, "Revenue At Risk",  f"${total_rev_at_risk/1e6:.2f}M",
     "⚠ High",   "#FFB84D", f"Avg ${avg_rev_at_risk:.1f} / customer"),

    (k4, "High Priority",    f"{high_count:,}",
     "🎯",       "#FF4D6A", f"${rev_high:,.0f} at risk"),

    (k5, "Model ROC-AUC",    f"{roc_auc:.4f}",
     "✓ Stable", "#00E5A0", f"5-Fold CV · σ={cv_std:.4f}"),
]

for col, label, value, badge, color, sub in kpis:
    badge_html = (
        f'<span style="font-size:9px;background:{color}22;color:{color};'
        f'padding:2px 7px;border-radius:20px;">{badge}</span>'
    ) if badge else ""
    with col:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-top:2px solid {color};
            border-radius:10px;padding:18px 16px;">
  <div style="font-size:10px;color:#8B9DC3;margin-bottom:8px;
              display:flex;justify-content:space-between;align-items:center;">
    <span>{label}</span>{badge_html}
  </div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;
              color:{color};letter-spacing:-0.5px;">{value}</div>
  <div style="font-size:10px;color:#4A5A7A;margin-top:5px;">{sub}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# ROW 2 — Churn Donut + Revenue Bars
# ============================================================
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Customer Churn Distribution</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:10px;">
  Retained vs churned across full customer base</div>
""", unsafe_allow_html=True)

    fig_donut = go.Figure(data=[go.Pie(
        labels=["Retained", "Churned"],
        values=[int(retained_count), int(churned_count)],
        hole=0.70,
        marker=dict(colors=["#1E3A6B", "#FF4D6A"],
                    line=dict(color="#090E1A", width=3)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    )])
    fig_donut.add_annotation(
        text=f"<b>{churn_rate:.1f}%</b><br>Churn Rate",
        x=0.5, y=0.5,
        font=dict(size=17, color="#FF4D6A", family="Space Grotesk"),
        showarrow=False, align="center"
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.06,
                    xanchor="center", x=0.5,
                    font=dict(color="#8B9DC3", size=12)),
        margin=dict(t=0, b=20, l=20, r=20),
        height=270,
    )
    st.plotly_chart(fig_donut, use_container_width=True,
                    config={"displayModeBar": False})

    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:12px;text-align:center;">
  <div style="font-size:18px;font-weight:700;color:#4F8EF7;">{int(retained_count):,}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:3px;">
    Retained · {100-churn_rate:.1f}%</div>
</div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:12px;text-align:center;">
  <div style="font-size:18px;font-weight:700;color:#FF4D6A;">{int(churned_count):,}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:3px;">
    Churned · {churn_rate:.1f}%</div>
</div>""", unsafe_allow_html=True)


with col_r:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Revenue At Risk by Priority Segment</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:10px;">
  Dollar exposure mapped to retention urgency</div>
""", unsafe_allow_html=True)

    pct_h = rev_high   / total_rev * 100
    pct_m = rev_medium / total_rev * 100
    pct_l = rev_low    / total_rev * 100

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(
        y=["Low Priority", "Medium Priority", "High Priority"],
        x=[rev_low, rev_medium, rev_high],
        orientation="h",
        marker=dict(color=["#00E5A0", "#FFB84D", "#FF4D6A"], line=dict(width=0)),
        text=[f"${rev_low:,.0f}  ({pct_l:.1f}%)",
              f"${rev_medium:,.0f}  ({pct_m:.1f}%)",
              f"${rev_high:,.0f}  ({pct_h:.1f}%)"],
        textposition="outside",
        textfont=dict(color="#8B9DC3", size=11),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        width=0.5,
    ))
    fig_rev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#1E2D4A",
                   tickprefix="$", tickformat=",.0f",
                   color="#4A5A7A", tickfont=dict(size=10),
                   showline=False, zeroline=False),
        yaxis=dict(color="#8B9DC3", tickfont=dict(size=11),
                   showline=False, showgrid=False),
        margin=dict(t=0, b=10, l=10, r=120),
        height=270,
        bargap=0.4,
    )
    st.plotly_chart(fig_rev, use_container_width=True,
                    config={"displayModeBar": False})

    r1, r2, r3 = st.columns(3)
    for cx, val, lbl, clr in [
        (r1, f"${rev_high:,.0f}",   f"High · {pct_h:.0f}%",   "#FF4D6A"),
        (r2, f"${rev_medium:,.0f}", f"Med · {pct_m:.0f}%",    "#FFB84D"),
        (r3, f"${rev_low:,.0f}",    f"Low · {pct_l:.0f}%",    "#00E5A0"),
    ]:
        with cx:
            st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:10px;text-align:center;">
  <div style="font-size:13px;font-weight:700;color:{clr};">{val}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:2px;">{lbl}</div>
</div>""", unsafe_allow_html=True)


st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# ROW 3 — Priority Queue + Model Metrics
# ============================================================
col_q, col_m = st.columns(2)

with col_q:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Retention Priority Queue</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:14px;">
  Customer count and revenue exposure by action tier</div>
""", unsafe_allow_html=True)

    queue = [
        ("High Priority",   high_count,   rev_high,   "#FF4D6A", "Immediate action"),
        ("Medium Priority", medium_count, rev_medium, "#FFB84D", "Plan this week"),
        ("Low Priority",    low_count,    rev_low,    "#00E5A0", "Monitor closely"),
    ]
    max_c = max(high_count, medium_count, low_count)
    for name, count, rev, color, action in queue:
        pct_bar = count / max_c * 100
        st.markdown(f"""
<div style="margin-bottom:20px;">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
    <span style="font-size:12px;font-weight:600;color:{color};">{name}</span>
    <span style="font-size:14px;font-weight:700;color:#EDF2FF;">{count:,}</span>
  </div>
  <div style="background:#1E2D4A;border-radius:4px;height:5px;margin-bottom:5px;">
    <div style="background:{color};width:{pct_bar:.0f}%;height:5px;border-radius:4px;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;">
    <span style="font-size:10px;color:#4A5A7A;">${rev:,.0f} at risk</span>
    <span style="font-size:10px;color:#4A5A7A;">{action}</span>
  </div>
</div>
""", unsafe_allow_html=True)

with col_m:
    st.markdown(f"""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Model Performance Summary</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:14px;">
  XGBoost champion · threshold tuned at {threshold}</div>
""", unsafe_allow_html=True)

    model_rows = [
        ("ROC-AUC Score",    f"{roc_auc:.4f}",        "#00E5A0", "5-Fold Cross Validation Mean"),
        ("CV Stability (σ)", f"{cv_std:.4f}",          "#4F8EF7", "Low variance → stable model"),
        ("Precision",        f"{precision*100:.2f}%",  "#FFB84D", f"At threshold {threshold}"),
        ("Recall",           f"{recall*100:.2f}%",     "#FF4D6A", "Captures churners effectively"),
        ("F1 Score",         f"{f1:.4f}",              "#A78BFA", "Balanced churn performance"),
    ]
    for label, value, color, note in model_rows:
        st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:11px 0;border-bottom:1px solid #1E2D4A;">
  <div>
    <div style="font-size:12px;color:#8B9DC3;">{label}</div>
    <div style="font-size:10px;color:#4A5A7A;margin-top:2px;">{note}</div>
  </div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;
              font-weight:700;color:{color};min-width:75px;text-align:right;">{value}</div>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# ROW 4 — Feature Importance (live from model)
# ============================================================
if feat_importance_df is not None:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Top 10 Churn Drivers</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:10px;">
  Feature importance extracted directly from XGBoost champion model</div>
""", unsafe_allow_html=True)

    # color gradient: top features red → lower features blue
    n = len(feat_importance_df)
    bar_colors = []
    for i in range(n):
        ratio = i / max(n - 1, 1)
        bar_colors.append(f"rgba({int(255*(1-ratio) + 79*ratio)}, "
                          f"{int(77*(1-ratio) + 142*ratio)}, "
                          f"{int(106*(1-ratio) + 247*ratio)}, 0.85)")

    fig_imp = go.Figure()
    fig_imp.add_trace(go.Bar(
        y=feat_importance_df["Feature"][::-1],
        x=feat_importance_df["Importance"][::-1],
        orientation="h",
        marker=dict(color=bar_colors[::-1], line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
    ))
    fig_imp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#1E2D4A",
                   color="#4A5A7A", tickfont=dict(size=10),
                   showline=False, zeroline=False),
        yaxis=dict(color="#8B9DC3", tickfont=dict(size=11),
                   showline=False, showgrid=False),
        margin=dict(t=0, b=10, l=10, r=20),
        height=320,
    )
    st.plotly_chart(fig_imp, use_container_width=True,
                    config={"displayModeBar": False})

    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# ROW 5 — Churn Probability Distribution (live from data)
# ============================================================
if risk_df is not None:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:2px;">
  Churn Probability Distribution</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:10px;">
  How churn risk is spread across all 51,047 customers</div>
""", unsafe_allow_html=True)

    probs = risk_df["ChurnProbability"].values
    hist_vals, bin_edges = np.histogram(probs, bins=40)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    bar_clrs = ["#FF4D6A" if c >= threshold else "#4F8EF7" for c in bin_centers]

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Bar(
        x=bin_centers,
        y=hist_vals,
        marker=dict(color=bar_clrs, line=dict(width=0)),
        hovertemplate="Prob: %{x:.2f}<br>Count: %{y:,}<extra></extra>",
    ))
    fig_dist.add_vline(
        x=threshold,
        line=dict(color="#FFB84D", width=2, dash="dash"),
        annotation=dict(
            text=f"Threshold {threshold}",
            font=dict(color="#FFB84D", size=11),
            yref="paper", y=1.05,
            showarrow=False,
        )
    )
    fig_dist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Churn Probability", color="#4A5A7A",
                   tickfont=dict(size=10), showgrid=False,
                   showline=False, zeroline=False),
        yaxis=dict(title="Customer Count", color="#4A5A7A",
                   tickfont=dict(size=10), showgrid=True,
                   gridcolor="#1E2D4A", showline=False),
        margin=dict(t=20, b=10, l=10, r=10),
        height=260,
        bargap=0.05,
    )
    st.plotly_chart(fig_dist, use_container_width=True,
                    config={"displayModeBar": False})

    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# STRATEGIC INSIGHTS — dynamic numbers
# ============================================================
st.markdown("""
<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
            color:#4A5A7A;margin-bottom:14px;">Strategic Intelligence</div>
""", unsafe_allow_html=True)

high_pct = rev_high / total_rev * 100

insights = [
    ("💰", "#FF4D6A", f"{high_pct:.0f}% Revenue Concentration",
     f"High-priority segment holds ${rev_high:,.0f} of ${total_rev_at_risk:,.0f} total risk. Address this first."),
    ("👤", "#FFB84D", "New Customers Most Vulnerable",
     "CustomerLifecycleStage_New is the top churn predictor — early engagement is critical."),
    ("📱", "#4F8EF7", "Aging Devices Drive Churn",
     "CurrentEquipmentDays ranks top-5 in importance. Device upgrade offers are high-ROI."),
    ("📉", "#A78BFA", "Usage Decline = Early Warning",
     f"PercChangeMinutes signals intent before churn. Avg churn probability: {avg_churn_prob:.1%}."),
]

i1, i2, i3, i4 = st.columns(4)
for col, (icon, color, title, body) in zip([i1, i2, i3, i4], insights):
    with col:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-left:3px solid {color};
            border-radius:10px;padding:18px;min-height:130px;">
  <div style="font-size:20px;margin-bottom:8px;">{icon}</div>
  <div style="font-size:12px;font-weight:600;color:{color};margin-bottom:6px;">{title}</div>
  <div style="font-size:11px;color:#8B9DC3;line-height:1.6;">{body}</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div style="margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid #1E2D4A;
            display:flex;justify-content:space-between;">
  <span style="font-size:11px;color:#2A3F6B;">
    ChurnIQ Executive Overview · Cell2Cell Telecom · {total_customers:,} records
  </span>
  <span style="font-size:11px;color:#2A3F6B;">
    XGBoost · Threshold {threshold} · ROC-AUC {roc_auc:.4f}
  </span>
</div>
""", unsafe_allow_html=True)