import streamlit as st
import pandas as pd
from pathlib import Path
from joblib import load

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🎯",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

model = load(
    BASE_DIR.parent.parent /
    "models" /
    "champion_xgboost.joblib"
)

st.title("🎯 Customer Churn Prediction")

st.success("Model Loaded Successfully")

st.subheader("Customer Inputs")

monthly_revenue = st.number_input(
    "Monthly Revenue",
    min_value=0.0,
    value=100.0
)

monthly_minutes = st.number_input(
    "Monthly Minutes",
    min_value=0.0,
    value=500.0
)

months_in_service = st.number_input(
    "Months In Service",
    min_value=0,
    value=12
)

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=35
)
import pandas as pd

if st.button("Predict Churn"):

    input_df = pd.DataFrame([{
        "MonthlyRevenue": monthly_revenue,
        "MonthlyMinutes": monthly_minutes,
        "MonthsInService": months_in_service,
        "AgeHH1": age
    }])

    st.write(input_df)