import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Revenue Risk Intelligence",
    page_icon="💰",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/revenue_risk_output.csv")

risk_df = load_data()

# ============================================================
# PAGE HEADER
# ============================================================

st.title("💰 Revenue Risk Intelligence")
st.caption("Identify revenue exposure, prioritize retention actions, and quantify business impact.")

st.markdown("---")

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue_at_risk = risk_df["RevenueRiskScore"].sum()

high_risk_customers = (
    risk_df["PrioritySegment"] == "High"
).sum()

avg_churn_probability = (
    risk_df["ChurnProbability"].mean()
)

highest_risk_score = (
    risk_df["RevenueRiskScore"].max()
)

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue At Risk",
        f"${total_revenue_at_risk:,.0f}"
    )

with col2:
    st.metric(
        "High Risk Customers",
        f"{high_risk_customers:,}"
    )

with col3:
    st.metric(
        "Avg Churn Probability",
        f"{avg_churn_probability:.2%}"
    )

with col4:
    st.metric(
        "Highest Risk Score",
        f"{highest_risk_score:.2f}"
    )

st.markdown("---")
# ============================================================
# PRIORITY SEGMENT DISTRIBUTION
# ============================================================

st.subheader("📊 Priority Segment Distribution")

segment_counts = (
    risk_df["PrioritySegment"]
    .value_counts()
    .reindex(["High", "Medium", "Low"])
    .reset_index()
)

segment_counts.columns = ["PrioritySegment", "Customers"]

fig = px.bar(
    segment_counts,
    x="Customers",
    y="PrioritySegment",
    orientation="h",
    text="Customers",
    title="Customer Distribution by Risk Segment"
)

fig.update_layout(
    height=450,
    template="plotly_dark",
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20)
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# ============================================================
# TOP REVENUE RISK CUSTOMERS
# ============================================================

st.subheader("🚨 Top Revenue Risk Customers")

st.caption(
    "Customers ranked by revenue exposure and churn likelihood."
)

top_risk_customers = (
    risk_df.sort_values(
        by="RevenueRiskScore",
        ascending=False
    )
    .head(10)
    .copy()
)

display_df = top_risk_customers[
    [
        "CustomerID",
        "MonthlyRevenue_Clean",
        "ChurnProbability",
        "RevenueRiskScore",
        "PrioritySegment"
    ]
]

display_df["MonthlyRevenue_Clean"] = (
    display_df["MonthlyRevenue_Clean"]
    .map(lambda x: f"${x:,.2f}")
)

display_df["ChurnProbability"] = (
    display_df["ChurnProbability"]
    .map(lambda x: f"{x:.2%}")
)

display_df["RevenueRiskScore"] = (
    display_df["RevenueRiskScore"]
    .map(lambda x: f"{x:.2f}")
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
# ============================================================
# REVENUE RECOVERY SIMULATOR
# ============================================================

st.subheader("🚀 Revenue Recovery Simulator")

st.caption(
    "Estimate potential revenue savings from retention campaigns."
)

# High Risk Customers Only
high_risk_df = risk_df[
    risk_df["PrioritySegment"] == "High"
]

high_risk_revenue = (
    high_risk_df["MonthlyRevenue_Clean"]
    .sum()
)

# Retention Slider
retention_rate = st.slider(
    "Retention Success Rate (%)",
    min_value=10,
    max_value=50,
    value=20,
    step=10
)

retention_rate_decimal = retention_rate / 100

# Calculations
recovered_revenue = (
    high_risk_revenue * retention_rate_decimal
)

customers_saved = int(
    len(high_risk_df) * retention_rate_decimal
)

annual_revenue_saved = (
    recovered_revenue * 12
)

st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Revenue Recovery",
        f"${recovered_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Customers Saved",
        f"{customers_saved:,}"
    )

with col3:
    st.metric(
        "Annual Revenue Protected",
        f"${annual_revenue_saved:,.0f}"
    )

st.markdown("---")
# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.subheader("🧠 Executive Insights")

high_risk_percentage = (
    (high_risk_customers / len(risk_df)) * 100
)

insight_1 = (
    f"📌 High-risk customers represent "
    f"**{high_risk_percentage:.1f}%** of the total customer base."
)

insight_2 = (
    f"📌 Total monthly revenue exposure is approximately "
    f"**${total_revenue_at_risk:,.0f}**."
)

insight_3 = (
    f"📌 At the current retention scenario "
    f"(**{retention_rate}%**), the business could protect "
    f"approximately **${annual_revenue_saved:,.0f} annually**."
)

insight_4 = (
    f"📌 Average churn probability across the customer portfolio "
    f"is **{avg_churn_probability:.2%}**."
)

insight_5 = (
    f"📌 The highest identified revenue risk score is "
    f"**{highest_risk_score:.2f}**, indicating a concentration "
    f"of revenue exposure among a small set of customers."
)

st.info(insight_1)
st.info(insight_2)
st.info(insight_3)
st.info(insight_4)
st.info(insight_5)

st.markdown("---")