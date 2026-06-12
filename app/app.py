import streamlit as st

st.set_page_config(
    page_title="ChurnIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 ChurnIQ")
st.subheader(
    "Predict. Prioritize. Retain."
)

st.markdown(
    """
    AI-Powered Telecom Customer Churn &
    Revenue Risk Intelligence Platform
    """
)

st.info(
    """
    Welcome to ChurnIQ.

    Use the sidebar to navigate through:
    - Executive Overview
    - Churn Prediction
    - Revenue Risk Analysis
    - Churn Drivers
    - Customer Prioritization
    - Strategic Recommendations
    """
)