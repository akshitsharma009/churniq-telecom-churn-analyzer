# ChurnIQ - features.py
# Feature engineering — model features ONLY

import pandas as pd
import numpy as np


def build_features(df):
    df = df.copy()

    # ── 1. charges_per_month_trend ──────────────────────────────
    # Total charges vs monthly charges ratio — detects billing anomalies
    if "totalcharges" in df.columns and "monthlycharges" in df.columns:
        df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
        df["totalcharges"].fillna(df["monthlycharges"], inplace=True)
        df["charges_per_month_trend"] = df["totalcharges"] / (df["monthlycharges"] + 1)
    else:
        df["charges_per_month_trend"] = 0

    # ── 2. product_to_charge_ratio ──────────────────────────────
    # Number of services vs monthly charge — value perception
    service_cols = [
        "phoneservice", "multiplelines", "internetservice",
        "onlinesecurity", "onlinebackup", "deviceprotection",
        "techsupport", "streamingtv", "streamingmovies"
    ]
    available_services = [c for c in service_cols if c in df.columns]
    df["service_count"] = df[available_services].apply(
        lambda row: sum(1 for v in row if str(v).lower() not in ["no", "no internet service", "no phone service"]),
        axis=1
    )
    df["product_to_charge_ratio"] = df["service_count"] / (df["monthlycharges"] + 1)

    # ── 3. engagement_score ─────────────────────────────────────
    # Higher services used = more engaged customer
    df["engagement_score"] = df["service_count"] / (len(available_services) + 1)

    # ── 4. contract_risk_score ──────────────────────────────────
    # Month-to-month = high risk, two year = low risk
    if "contract" in df.columns:
        contract_map = {
            "month-to-month": 3,
            "one_year": 2,
            "one year": 2,
            "two_year": 1,
            "two year": 1
        }
        df["contract_risk_score"] = df["contract"].str.lower().map(contract_map).fillna(2)
    else:
        df["contract_risk_score"] = 2

    # ── 5. tenure_segment ───────────────────────────────────────
    if "tenure" in df.columns:
        df["tenure_months"] = df["tenure"]
        df["tenure_segment"] = pd.cut(
            df["tenure_months"],
            bins=[0, 12, 24, 36, np.inf],
            labels=["new", "developing", "established", "loyal"],
            right=True
        ).astype(str)
    else:
        df["tenure_months"] = 0
        df["tenure_segment"] = "unknown"

    # ── 6. price_sensitivity_flag ───────────────────────────────
    # High monthly charge + month-to-month = price sensitive
    charge_threshold = df["monthlycharges"].quantile(0.75)
    df["price_sensitivity_flag"] = (
        (df["monthlycharges"] > charge_threshold) &
        (df.get("contract", pd.Series([""] * len(df))).str.lower() == "month-to-month")
    ).astype(int)

    # ── 7. loyalty_score ────────────────────────────────────────
    # Tenure normalized 0-1
    max_tenure = df["tenure_months"].max() if df["tenure_months"].max() > 0 else 1
    df["loyalty_score"] = df["tenure_months"] / max_tenure

    # ── 8. monthly_charge_tier ──────────────────────────────────
    df["monthly_charge_tier"] = pd.cut(
        df["monthlycharges"],
        bins=[0, 35, 65, 95, np.inf],
        labels=[1, 2, 3, 4],
        right=True
    ).astype(float)

    # ── 9. support_dependency_score ─────────────────────────────
    support_cols = ["techsupport", "onlinesecurity", "onlinebackup", "deviceprotection"]
    available_support = [c for c in support_cols if c in df.columns]
    df["support_dependency_score"] = df[available_support].apply(
        lambda row: sum(1 for v in row if str(v).lower() == "yes"),
        axis=1
    ) / (len(available_support) + 1)

    # ── 10. payment_risk_flag ───────────────────────────────────
    if "paymentmethod" in df.columns:
        df["payment_risk_flag"] = df["paymentmethod"].str.lower().apply(
            lambda x: 1 if "electronic check" in str(x) else 0
        )
    else:
        df["payment_risk_flag"] = 0

    print("✅ Features built successfully")
    return df


def get_model_features():
    return [
        "charges_per_month_trend",
        "product_to_charge_ratio",
        "engagement_score",
        "contract_risk_score",
        "tenure_segment",
        "price_sensitivity_flag",
        "loyalty_score",
        "monthly_charge_tier",
        "support_dependency_score",
        "payment_risk_flag"
    ]