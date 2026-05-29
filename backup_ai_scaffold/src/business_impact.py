# ChurnIQ - business_impact.py
# Business decision layer — revenue risk + retention economics

import pandas as pd
import numpy as np
import yaml


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def calculate_business_metrics(df):
    config = load_config()
    biz = config["business"]

    df = df.copy()

    avg_lifetime = biz["avg_customer_lifetime"]
    cost_multipliers = biz["retention_cost_multiplier"]
    risk_tiers = biz["risk_tiers"]

    # ── LAYER 2: Future Revenue Risk ────────────────────────────

    df["expected_remaining_months"] = df["tenure_months"].apply(
        lambda t: max(0, avg_lifetime - t)
    )

    df["future_revenue_loss"] = (
        df["monthly_charges"] * df["expected_remaining_months"]
    )

    df["revenue_at_risk"] = (
        df["churn_probability"] * df["future_revenue_loss"]
    )

    # ── LAYER 3: Retention Economics ────────────────────────────

    def get_retention_cost(row):
        contract = str(row.get("contract_type", "month-to-month")).lower().strip()
        monthly = row["monthly_charges"]

        if "two" in contract:
            return monthly * cost_multipliers["two_year"]
        elif "one" in contract:
            return monthly * cost_multipliers["one_year"]
        else:
            return monthly * cost_multipliers["month-to-month"]

    df["retention_cost"] = df.apply(get_retention_cost, axis=1)

    df["net_retention_value"] = (
        df["revenue_at_risk"] - df["retention_cost"]
    )

    df["retention_roi"] = df.apply(
        lambda row: row["net_retention_value"] / row["retention_cost"]
        if row["retention_cost"] > 0 else 0,
        axis=1
    )

    df["priority_score"] = (
        df["net_retention_value"] * df["churn_probability"]
    )

    df["is_worth_retaining"] = (
        df["net_retention_value"] > 0
    ).astype(int)

    # ── LAYER 1: Risk Tier ───────────────────────────────────────

    def get_risk_tier(prob):
        if prob >= risk_tiers["high"]:
            return "HIGH"
        elif prob >= risk_tiers["medium"]:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk_tier"] = df["churn_probability"].apply(get_risk_tier)

    # ── LAYER 4: Retention Decision Engine ──────────────────────

    df = apply_retention_decision(df)

    print("✅ Business metrics calculated")
    return df


def get_churn_driver(shap_values, feature_names):
    """Get top SHAP driver per customer"""
    if shap_values is None:
        return "price_sensitivity"

    top_idx = np.abs(shap_values).argmax(axis=1)
    drivers = [feature_names[i] for i in top_idx]
    return drivers


def map_driver_to_category(driver):
    """Map feature name to business driver category"""
    mapping = {
        "charges_per_month_trend":   "price_sensitivity",
        "product_to_charge_ratio":   "price_sensitivity",
        "monthly_charge_tier":       "price_sensitivity",
        "price_sensitivity_flag":    "price_sensitivity",
        "contract_risk_score":       "contract_risk",
        "tenure_segment":            "tenure_segment",
        "loyalty_score":             "loyalty_score",
        "engagement_score":          "low_engagement",
        "support_dependency_score":  "support_dependency",
        "payment_risk_flag":         "payment_risk",
    }
    return mapping.get(driver, "price_sensitivity")


def apply_retention_decision(df):
    """Apply retention matrix based on risk tier + churn driver"""

    retention_matrix = {
        ("HIGH",   "price_sensitivity"):  ("20% discount",             "URGENT", "Phone"),
        ("HIGH",   "contract_risk"):      ("Annual plan incentive",     "URGENT", "SMS + App"),
        ("HIGH",   "low_engagement"):     ("Personal account manager",  "HIGH",   "Email"),
        ("MEDIUM", "support_dependency"): ("Free tech support",         "MEDIUM", "App"),
        ("MEDIUM", "payment_risk"):       ("Auto-pay cashback",         "MEDIUM", "SMS"),
        ("MEDIUM", "price_sensitivity"):  ("Plan downgrade suggestion", "MEDIUM", "App"),
        ("LOW",    "tenure_segment"):     ("Loyalty reward",            "LOW",    "App"),
        ("LOW",    "loyalty_score"):      ("Appreciation + points",     "LOW",    "Email"),
    }

    default_action = ("Monitor customer",  "LOW", "App")

    def get_action(row):
        tier = row.get("risk_tier", "LOW")
        driver = row.get("churn_driver_category", "price_sensitivity")
        return retention_matrix.get((tier, driver), default_action)

    # If churn_driver_category not yet set, use default
    if "churn_driver_category" not in df.columns:
        df["churn_driver_category"] = "price_sensitivity"

    actions = df.apply(get_action, axis=1)
    df["retention_action"] = actions.apply(lambda x: x[0])
    df["urgency"]           = actions.apply(lambda x: x[1])
    df["contact_channel"]   = actions.apply(lambda x: x[2])

    return df