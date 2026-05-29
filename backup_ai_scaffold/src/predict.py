# ChurnIQ - predict.py
# Prediction pipeline — single customer + batch

import pandas as pd
import numpy as np
import pickle
import yaml
import os

from src.features import build_features, get_model_features
from src.business_impact import calculate_business_metrics


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_model():
    config = load_config()
    model_path = os.path.join(config["paths"]["models"], "best_model.pkl")
    le_path = os.path.join(config["paths"]["models"], "feature_pipeline.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(le_path, "rb") as f:
        label_encoder = pickle.load(f)

    return model, label_encoder


def preprocess_for_prediction(df, label_encoder):
    df = build_features(df)
    features = get_model_features()

    # Encode tenure_segment
    df["tenure_segment"] = label_encoder.transform(
        df["tenure_segment"].astype(str)
    )

    X = df[features]
    return X, df


def predict_batch(df):
    model, label_encoder = load_model()

    X, df_feat = preprocess_for_prediction(df, label_encoder)

    df_feat["churn_probability"] = model.predict_proba(X)[:, 1]
    df_feat["churn_predicted"] = model.predict(X)

    # Map monthly_charges if needed
    if "monthlycharges" in df_feat.columns and "monthly_charges" not in df_feat.columns:
        df_feat["monthly_charges"] = df_feat["monthlycharges"]

    if "contract" in df_feat.columns and "contract_type" not in df_feat.columns:
        df_feat["contract_type"] = df_feat["contract"]

    df_result = calculate_business_metrics(df_feat)

    print(f"✅ Batch prediction complete — {len(df_result)} customers")
    return df_result


def predict_single(customer_dict):
    """
    Input: dict with raw customer fields
    Output: dict with churn probability + all business metrics
    """
    df = pd.DataFrame([customer_dict])
    result = predict_batch(df)
    row = result.iloc[0]

    output = {
        "churn_probability":        round(float(row["churn_probability"]), 4),
        "churn_predicted":          int(row["churn_predicted"]),
        "risk_tier":                row["risk_tier"],
        "expected_remaining_months": int(row["expected_remaining_months"]),
        "future_revenue_loss":      round(float(row["future_revenue_loss"]), 2),
        "revenue_at_risk":          round(float(row["revenue_at_risk"]), 2),
        "retention_cost":           round(float(row["retention_cost"]), 2),
        "net_retention_value":      round(float(row["net_retention_value"]), 2),
        "retention_roi":            round(float(row["retention_roi"]), 4),
        "priority_score":           round(float(row["priority_score"]), 4),
        "is_worth_retaining":       int(row["is_worth_retaining"]),
        "retention_action":         row["retention_action"],
        "urgency":                  row["urgency"],
        "contact_channel":          row["contact_channel"],
    }

    return output