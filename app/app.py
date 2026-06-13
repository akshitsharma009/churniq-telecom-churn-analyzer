import streamlit as st

st.set_page_config(
    page_title="ChurnIQ — Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS
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

/* page links in sidebar */
[data-testid="stSidebarNav"] a {
    color: #8B9DC3 !important;
    font-size: 13px !important;
}
[data-testid="stSidebarNav"] a:hover {
    color: #EDF2FF !important;
    background: #1E2D4A !important;
}

/* metric overrides */
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}
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

    st.page_link("app.py",                         label="🏠  Home")
    st.page_link("pages/1_Executive_Overview.py",  label="📊  Executive Overview")

    st.markdown("""
<hr style="border:none;border-top:1px solid #1E2D4A;margin:1.5rem 0 1.2rem 0;">
<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#4A5A7A;margin-bottom:10px;">
  Model Info
</div>
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
# HERO — using native st elements so no raw-HTML rendering bug
# ============================================================

st.markdown("""
<div style="margin-top:1rem;margin-bottom:0.5rem;">
  <span style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#4F8EF7;">
    Telecom Revenue Intelligence
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:46px;font-weight:700;
            color:#EDF2FF;letter-spacing:-2px;line-height:1;margin-bottom:16px;">
  Churn<span style="color:#4F8EF7;">IQ</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="font-size:16px;color:#8B9DC3;max-width:580px;line-height:1.75;margin:0 0 2.5rem 0;">
  End-to-end ML platform that identifies at-risk customers, quantifies revenue exposure,
  and prioritizes retention — before churn happens.
</p>
""", unsafe_allow_html=True)


# ============================================================
# STAT TILES
# ============================================================

c1, c2, c3, c4 = st.columns(4)

tiles = [
    (c1, "51,047",  "Customers Analyzed", "#4F8EF7"),
    (c2, "$1.38M",  "Revenue At Risk",    "#FF4D6A"),
    (c3, "28.82%",  "Churn Rate",         "#FFB84D"),
    (c4, "0.68",    "Model ROC-AUC",      "#00E5A0"),
]

for col, val, label, color in tiles:
    with col:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-top:2px solid {color};
            border-radius:10px;padding:22px 20px;text-align:center;">
  <div style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;
              color:{color};letter-spacing:-0.5px;">{val}</div>
  <div style="font-size:11px;color:#8B9DC3;margin-top:5px;">{label}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)


# ============================================================
# MODULE CARDS
# ============================================================

st.markdown("""
<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#4A5A7A;margin-bottom:6px;">
  Platform Modules
</div>
<div style="font-size:22px;font-weight:600;color:#EDF2FF;margin-bottom:18px;">
  What ChurnIQ delivers
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊", "Executive Overview",
     "KPIs, churn distribution, revenue risk breakdown, and priority segmentation at a glance.",
     "#4F8EF7"),
    ("🎯", "Churn Prediction",
     "XGBoost-powered churn probability scores for every customer with threshold-tuned decisions.",
     "#00D4FF"),
    ("💰", "Revenue Risk Engine",
     "Monetize churn risk. Every at-risk dollar quantified and mapped to actionable segments.",
     "#FF4D6A"),
    ("🔍", "Churn Drivers",
     "SHAP-level feature importance revealing what actually drives customers to leave.",
     "#FFB84D"),
    ("⚡", "Retention Prioritization",
     "High / Medium / Low priority queues so retention teams focus where it counts most.",
     "#00E5A0"),
    ("📋", "Strategic Playbook",
     "Data-backed recommendations translated into business actions, not just model outputs.",
     "#A78BFA"),
]

r1 = st.columns(3)
r2 = st.columns(3)

for i, (icon, title, desc, color) in enumerate(modules):
    col = r1[i] if i < 3 else r2[i - 3]
    with col:
        st.markdown(f"""
<div style="background:#141C33;border:1px solid #1E2D4A;border-left:3px solid {color};
            border-radius:10px;padding:22px;margin-bottom:12px;">
  <div style="font-size:24px;margin-bottom:10px;">{icon}</div>
  <div style="font-size:13px;font-weight:600;color:{color};margin-bottom:7px;">{title}</div>
  <div style="font-size:12px;color:#8B9DC3;line-height:1.65;">{desc}</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="margin-top:3rem;padding-top:1.2rem;border-top:1px solid #1E2D4A;
            display:flex;justify-content:space-between;">
  <span style="font-size:11px;color:#2A3F6B;">ChurnIQ · Built with XGBoost + Streamlit</span>
  <span style="font-size:11px;color:#2A3F6B;">Cell2Cell · 51,047 records · Production-Ready</span>
</div>
""", unsafe_allow_html=True)