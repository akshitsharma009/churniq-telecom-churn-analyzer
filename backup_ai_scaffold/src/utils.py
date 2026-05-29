# ChurnIQ - utils.py
# Helper functions — reusable utilities

import pandas as pd
import numpy as np
import yaml
import os
import pickle
from datetime import datetime


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dirs():
    """Create all required directories if not exist"""
    dirs = [
        "data/raw",
        "data/processed",
        "database/queries",
        "notebooks",
        "src",
        "models",
        "reports/figures",
        "app/pages",
        "config"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ All directories verified")


def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f"✅ Saved: {path}")


def load_pickle(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def get_churn_rate(df, target="churn"):
    rate = df[target].mean() * 100
    return round(rate, 2)


def get_revenue_summary(df):
    summary = {
        "total_revenue_at_risk":     round(df["revenue_at_risk"].sum(), 2),
        "avg_revenue_at_risk":       round(df["revenue_at_risk"].mean(), 2),
        "total_priority_score":      round(df["priority_score"].sum(), 2),
        "worth_retaining_count":     int(df["is_worth_retaining"].sum()),
        "not_worth_retaining_count": int((df["is_worth_retaining"] == 0).sum()),
        "high_risk_count":           int((df["risk_tier"] == "HIGH").sum()),
        "medium_risk_count":         int((df["risk_tier"] == "MEDIUM").sum()),
        "low_risk_count":            int((df["risk_tier"] == "LOW").sum()),
    }
    return summary


def format_currency(value):
    return f"${value:,.2f}"


def format_percent(value):
    return f"{value:.2f}%"


def log_step(step_name, message=""):
    ts = get_timestamp()
    print(f"[{ts}] ▶ {step_name} {message}")


def validate_features(df, required_features):
    missing = [f for f in required_features if f not in df.columns]
    if missing:
        print(f"⚠️ Missing features: {missing}")
        return False
    print("✅ All required features present")
    return True