import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Executive Overview",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/feature_engineered.csv"
)

# ==========================================
# KPI METRICS
# ==========================================

total_customers = len(df)

churn_rate = (
    (df["Churn"] == "Yes").mean()
    * 100
)

total_revenue_at_risk = 1379824.99

high_priority_customers = 17016

# ==========================================
# PAGE HEADER
# ==========================================

st.title("📈 Executive Overview")

st.markdown(
    """
    Real-time business overview of customer churn,
    revenue exposure, and retention priorities.
    """
)

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col3:
    st.metric(
        "Revenue At Risk",
        f"${total_revenue_at_risk:,.0f}"
    )

with col4:
    st.metric(
        "High Priority",
        f"{high_priority_customers:,}"
    )

with col5:
    st.metric(
        "Champion Model",
        "XGBoost"
    )

    # ==========================================
# CHURN DISTRIBUTION
# ==========================================

churn_counts = (
    df["Churn"]
    .value_counts()
    .reset_index()
)

churn_counts.columns = [
    "Churn",
    "Count"
]

fig = px.pie(
    churn_counts,
    names="Churn",
    values="Count",
    hole=0.6,
    title="Customer Churn Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:

    segment_df = pd.DataFrame({
        "Segment": ["High", "Medium", "Low"],
        "Customers": [17016, 17015, 17016]
    })

    fig_segment = px.bar(
        segment_df,
        x="Segment",
        y="Customers",
        title="Priority Segment Distribution"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

with col2:

    revenue_df = pd.DataFrame({
        "Segment": ["High", "Medium", "Low"],
        "RevenueRisk": [
            829584,
            367727,
            182514
        ]
    })

    fig_revenue = px.bar(
        revenue_df,
        x="Segment",
        y="RevenueRisk",
        title="Revenue At Risk by Segment"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

    st.markdown("## Strategic Insights")

st.success("""
• High-priority customers account for ~60% of total revenue risk.

• New customers are the strongest churn segment.

• Aging devices significantly increase churn probability.

• Usage decline acts as an early warning signal.

• Total revenue currently at risk exceeds $1.38M.
""")