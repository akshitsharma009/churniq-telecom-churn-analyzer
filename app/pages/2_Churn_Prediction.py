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

# ==================================
# DEFAULT RESULTS
# ==================================

churn_probability = "--"
risk_level = "--"
revenue_exposure = "--"
recommendation = "--"

# ==================================
# HEADER
# ==================================

st.title("🎯 Customer Churn Prediction")
# ==================================
# SESSION STATE
# ==================================



# ==================================
# RESULT CARDS
# ==================================



# ==================================
# INPUTS
# ==================================

left, right = st.columns(2)

with left:

    st.subheader("👤 Customer Profile")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    months_in_service = st.number_input(
        "Months In Service",
        min_value=0,
        value=24
    )

    lifecycle = st.selectbox(
        "Customer Lifecycle Stage",
        ["New", "Growing", "Loyal"]
    )

    marital = st.selectbox(
        "Marital Status",
        ["Yes", "No", "Unknown"]
    )

    st.subheader("📈 Usage Metrics")

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

with right:

    st.subheader("📱 Device Metrics")

    equipment_days = st.number_input(
        "Current Equipment Days",
        min_value=0,
        value=365
    )

    handset_models = st.number_input(
        "Handset Models",
        min_value=1,
        value=1
    )

    handset_refurb = st.selectbox(
        "Handset Refurbished",
        ["Yes", "No"]
    )

    handset_web = st.selectbox(
        "Handset Web Capable",
        ["Yes", "No"]
    )

    st.subheader("🤝 Relationship Metrics")

    credit_rating = st.selectbox(
        "Credit Rating",
        [1, 2, 3, 4, 5, 6, 7]
    )

    region = st.selectbox(
        "Region Code",
        [
            "SEA","PIT","MIL","OKC","SAN",
            "SLC","LOU","KCY","DEN","PHI"
        ]
    )

st.divider()

if st.button(
    "🎯 Predict Churn",
    use_container_width=True
):

    template = pd.read_csv(
        BASE_DIR.parent.parent /
        "data" /
        "processed" /
        "feature_engineered.csv",
        nrows=1,
        low_memory=False
    )

    input_df = template.copy()

    input_df["MonthlyRevenue"] = monthly_revenue
    input_df["MonthlyMinutes"] = monthly_minutes
    input_df["MonthsInService"] = months_in_service
    input_df["AgeHH1"] = age

    input_df["CurrentEquipmentDays"] = equipment_days
    input_df["HandsetModels"] = handset_models

    input_df["HandsetRefurbished"] = handset_refurb
    input_df["HandsetWebCapable"] = handset_web

    input_df["CustomerLifecycleStage"] = lifecycle
    input_df["MaritalStatus"] = marital

    input_df["CreditRating_Encoded"] = credit_rating
    input_df["RegionCode"] = region

    input_df = input_df.drop(
        columns=["CustomerID", "Churn"],
        errors="ignore"
    )

    probability = model.predict_proba(input_df)[0][1]

    if probability >= 0.70:
        risk_level = "🔴 High"
        recommendation = "Immediate Retention Action"

    elif probability >= 0.40:
        risk_level = "🟡 Medium"
        recommendation = "Targeted Offer"

    else:
        risk_level = "🟢 Low"
        recommendation = "Monitor"

    revenue_exposure = monthly_revenue * probability

    st.success("Prediction Generated Successfully")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Churn Probability",
            f"{probability:.1%}"
        )

    with c2:
        st.metric(
            "Risk Level",
            risk_level
        )

    with c3:
        st.metric(
            "Revenue Exposure",
            f"${revenue_exposure:,.2f}"
        )

    with c4:
        st.metric(
            "Recommendation",
            recommendation
        )

    st.divider()

    st.subheader("🔍 Why This Customer Is Risky")

    risk_factors = []

    if lifecycle == "New":
        risk_factors.append(
            "⚠ New customers historically show higher churn risk."
        )

    if months_in_service < 12:
        risk_factors.append(
            "⚠ Customer tenure is relatively low."
        )

    if credit_rating <= 2:
        risk_factors.append(
            "⚠ Low credit rating increases churn probability."
        )

    if handset_refurb == "Yes":
        risk_factors.append(
            "⚠ Refurbished handset usage is associated with higher churn."
        )

    if equipment_days > 700:
        risk_factors.append(
            "⚠ Device age may indicate upgrade dissatisfaction."
        )

    if probability > 0.60:
        risk_factors.append(
            "⚠ Model predicted a high likelihood of churn."
        )

    if not risk_factors:
        risk_factors.append(
            "✅ No major churn indicators detected."
        )

    for factor in risk_factors:
        st.info(factor)