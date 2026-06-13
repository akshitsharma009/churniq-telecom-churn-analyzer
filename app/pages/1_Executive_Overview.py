import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

/* Remove plotly chart top whitespace */
.js-plotly-plot .plotly { margin-top: 0 !important; }
iframe { border: none !important; }
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

    st.markdown("""
<hr style="border:none;border-top:1px solid #1E2D4A;margin:1.5rem 0 1.2rem 0;">
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;padding:14px;">
  <div style="font-size:10px;color:#8B9DC3;margin-bottom:3px;">Champion Model</div>
  <div style="font-size:15px;font-weight:600;color:#4F8EF7;">XGBoost</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:10px;margin-bottom:3px;">ROC-AUC Score</div>
  <div style="font-size:15px;font-weight:600;color:#00E5A0;">0.6800</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:10px;margin-bottom:3px;">Decision Threshold</div>
  <div style="font-size:15px;font-weight:600;color:#FFB84D;">0.40</div>
</div>
<div style="font-size:10px;color:#2A3F6B;text-align:center;margin-top:2rem;">
  Cell2Cell Dataset · 51,047 records
</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA DYNAMICALLY
# ============================================================
@st.cache_data
def load_risk_data():
    df = pd.read_csv("data/processed/revenue_risk_output.csv")
    return df

@st.cache_data
def load_feature_data():
    df = pd.read_csv("data/processed/feature_engineered.csv")
    return df

try:
    risk_df = load_risk_data()

    total_customers       = len(risk_df)
    total_revenue_at_risk = risk_df["RevenueRiskScore"].sum()
    churned_count         = (risk_df["ChurnProbability"] >= 0.40).sum()
    churn_rate            = churned_count / total_customers * 100
    retained_count        = total_customers - churned_count

    seg_counts   = risk_df["PrioritySegment"].value_counts()
    high_count   = int(seg_counts.get("High",   0))
    medium_count = int(seg_counts.get("Medium", 0))
    low_count    = int(seg_counts.get("Low",    0))

    seg_rev      = risk_df.groupby("PrioritySegment")["RevenueRiskScore"].sum()
    rev_high     = seg_rev.get("High",   0)
    rev_medium   = seg_rev.get("Medium", 0)
    rev_low      = seg_rev.get("Low",    0)

    data_ok = True

except Exception as e:
    st.error(f"Data load error: {e}")
    # fallback to known values
    total_customers       = 51047
    total_revenue_at_risk = 1_379_824.99
    churn_rate            = 28.82
    churned_count         = 14711
    retained_count        = 36336
    high_count            = 17016
    medium_count          = 17015
    low_count             = 17016
    rev_high              = 829_584
    rev_medium            = 367_727
    rev_low               = 182_514
    data_ok = False


# ============================================================
# PAGE HEADER
# ============================================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
<div style="margin-bottom:1.5rem;">
  <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#4F8EF7;margin-bottom:6px;">
    ChurnIQ · Executive Overview
  </div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;
              color:#EDF2FF;letter-spacing:-0.5px;">
    Business Intelligence Summary
  </div>
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
  {'<div style="font-size:9px;color:#00E5A0;margin-top:4px;">● Live Data</div>' if data_ok else '<div style="font-size:9px;color:#FFB84D;margin-top:4px;">● Fallback Data</div>'}
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #1E2D4A;margin-bottom:1.5rem;'>", unsafe_allow_html=True)


# ============================================================
# KPI CARDS
# ============================================================
st.markdown("""
<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
            color:#4A5A7A;margin-bottom:12px;">Key Performance Indicators</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    (k1, "Total Customers",  f"{total_customers:,}",                     None,      "#4F8EF7", "Full analyzed base"),
    (k2, "Churn Rate",       f"{churn_rate:.2f}%",                       "▲ Risk",  "#FF4D6A", f"{churned_count:,} customers"),
    (k3, "Revenue At Risk",  f"${total_revenue_at_risk/1e6:.2f}M",       "⚠ High",  "#FFB84D", "Across all segments"),
    (k4, "High Priority",    f"{high_count:,}",                          "🎯",      "#FF4D6A", "Immediate action needed"),
    (k5, "Model ROC-AUC",    "0.6800",                                   "✓ Stable","#00E5A0", "5-Fold CV · σ=0.004"),
]

for col, label, value, badge, color, sub in kpis:
    badge_html = (f'<span style="font-size:9px;background:{color}22;color:{color};'
                  f'padding:2px 7px;border-radius:20px;">{badge}</span>') if badge else ""
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
# ROW 2 — Donut + Revenue Bars  (NO wrapper divs around charts)
# ============================================================
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:4px;">
  Customer Churn Distribution
</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:12px;">
  Retained vs churned across full customer base
</div>
""", unsafe_allow_html=True)

    fig_donut = go.Figure(data=[go.Pie(
        labels=["Retained", "Churned"],
        values=[retained_count, churned_count],
        hole=0.70,
        marker=dict(colors=["#1E3A6B", "#FF4D6A"],
                    line=dict(color="#090E1A", width=3)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    )])
    fig_donut.add_annotation(
        text=f"<b>{churn_rate:.1f}%</b><br><span style='font-size:11px'>Churn Rate</span>",
        x=0.5, y=0.5,
        font=dict(size=18, color="#FF4D6A", family="Space Grotesk"),
        showarrow=False, align="center"
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.08,
                    xanchor="center", x=0.5,
                    font=dict(color="#8B9DC3", size=12)),
        margin=dict(t=0, b=30, l=20, r=20),
        height=280,
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # stat row below donut
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:12px;text-align:center;">
  <div style="font-size:18px;font-weight:700;color:#4F8EF7;">{retained_count:,}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:3px;">Retained · {100-churn_rate:.1f}%</div>
</div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:12px;text-align:center;">
  <div style="font-size:18px;font-weight:700;color:#FF4D6A;">{churned_count:,}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:3px;">Churned · {churn_rate:.1f}%</div>
</div>""", unsafe_allow_html=True)


with col_r:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:4px;">
  Revenue At Risk by Priority Segment
</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:12px;">
  Dollar exposure mapped to retention urgency
</div>
""", unsafe_allow_html=True)

    total_rev = rev_high + rev_medium + rev_low
    pct_h = rev_high   / total_rev * 100
    pct_m = rev_medium / total_rev * 100
    pct_l = rev_low    / total_rev * 100

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(
        y=["Low Priority", "Medium Priority", "High Priority"],
        x=[rev_low, rev_medium, rev_high],
        orientation="h",
        marker=dict(color=["#00E5A0", "#FFB84D", "#FF4D6A"],
                    line=dict(width=0)),
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
        margin=dict(t=0, b=10, l=10, r=110),
        height=280,
        bargap=0.4,
    )
    st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})

    r1, r2, r3 = st.columns(3)
    for col_x, val, label, color in [
        (r1, f"${rev_high:,.0f}",   f"High · {pct_h:.0f}%",   "#FF4D6A"),
        (r2, f"${rev_medium:,.0f}", f"Medium · {pct_m:.0f}%", "#FFB84D"),
        (r3, f"${rev_low:,.0f}",    f"Low · {pct_l:.0f}%",    "#00E5A0"),
    ]:
        with col_x:
            st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-radius:8px;
            padding:10px;text-align:center;">
  <div style="font-size:13px;font-weight:700;color:{color};">{val}</div>
  <div style="font-size:10px;color:#8B9DC3;margin-top:2px;">{label}</div>
</div>""", unsafe_allow_html=True)


st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# ROW 3 — Priority Queue + Model Performance
# ============================================================
col_q, col_m = st.columns(2)

with col_q:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:4px;">
  Retention Priority Queue
</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:16px;">
  Customer count and revenue exposure by action tier
</div>
""", unsafe_allow_html=True)

    queue_items = [
        ("High Priority",   high_count,   rev_high,   "#FF4D6A", "Immediate action"),
        ("Medium Priority", medium_count, rev_medium, "#FFB84D", "Plan this week"),
        ("Low Priority",    low_count,    rev_low,    "#00E5A0", "Monitor closely"),
    ]
    max_c = max(high_count, medium_count, low_count)
    for name, count, rev, color, action in queue_items:
        pct = count / max_c * 100
        st.markdown(f"""
<div style="margin-bottom:20px;">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
    <span style="font-size:12px;font-weight:600;color:{color};">{name}</span>
    <span style="font-size:14px;font-weight:700;color:#EDF2FF;">{count:,}</span>
  </div>
  <div style="background:#1E2D4A;border-radius:4px;height:5px;margin-bottom:5px;">
    <div style="background:{color};width:{pct:.0f}%;height:5px;border-radius:4px;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;">
    <span style="font-size:10px;color:#4A5A7A;">${rev:,.0f} at risk</span>
    <span style="font-size:10px;color:#4A5A7A;">{action}</span>
  </div>
</div>
""", unsafe_allow_html=True)


with col_m:
    st.markdown("""
<div style="font-size:12px;font-weight:600;color:#EDF2FF;margin-bottom:4px;">
  Model Performance Summary
</div>
<div style="font-size:11px;color:#4A5A7A;margin-bottom:16px;">
  XGBoost champion · threshold tuned at 0.40
</div>
""", unsafe_allow_html=True)

    model_metrics = [
        ("ROC-AUC Score",    "0.6800", "#00E5A0", "5-Fold Cross Validation Mean"),
        ("CV Stability (σ)", "0.0044", "#4F8EF7", "Low variance → stable model"),
        ("Precision @ 0.40", "35.35%", "#FFB84D", "Churn detection precision"),
        ("Recall @ 0.40",    "82.66%", "#FF4D6A", "Captures 4 in 5 churners"),
        ("F1 Score @ 0.40",  "0.4952", "#A78BFA", "Balanced churn performance"),
    ]
    for label, value, color, note in model_metrics:
        st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:11px 0;border-bottom:1px solid #1E2D4A;">
  <div>
    <div style="font-size:12px;color:#8B9DC3;">{label}</div>
    <div style="font-size:10px;color:#4A5A7A;margin-top:2px;">{note}</div>
  </div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;
              font-weight:700;color:{color};min-width:70px;text-align:right;">{value}</div>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# STRATEGIC INSIGHTS
# ============================================================
st.markdown("""
<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
            color:#4A5A7A;margin-bottom:14px;">Strategic Intelligence</div>
""", unsafe_allow_html=True)

insights = [
    ("💰", "#FF4D6A", "60% Revenue Concentration",
     f"High-priority segment holds ${rev_high:,.0f} of ${total_revenue_at_risk:,.0f} total risk. Address this first."),
    ("👤", "#FFB84D", "New Customers Most Vulnerable",
     "CustomerLifecycleStage_New is the top churn predictor — early engagement is critical."),
    ("📱", "#4F8EF7", "Aging Devices Drive Churn",
     "CurrentEquipmentDays ranks top-5 in importance. Device upgrade offers are high-ROI."),
    ("📉", "#A78BFA", "Usage Decline = Early Warning",
     "PercChangeMinutes signals intent before churn. Act within 30 days of usage drop."),
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
st.markdown("""
<div style="margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid #1E2D4A;
            display:flex;justify-content:space-between;">
  <span style="font-size:11px;color:#2A3F6B;">ChurnIQ Executive Overview · Cell2Cell Telecom Dataset</span>
  <span style="font-size:11px;color:#2A3F6B;">XGBoost Champion · Threshold 0.40 · Production-Ready</span>
</div>
""", unsafe_allow_html=True)