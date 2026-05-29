# ChurnIQ - database.py
# SQLite database operations — sqlite3 ONLY

import sqlite3
import pandas as pd
import yaml
import os


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_connection():
    config = load_config()
    db_path = config["paths"]["database"]
    conn = sqlite3.connect(db_path)
    return conn


def init_db():
    config = load_config()
    schema_path = "database/schema.sql"
    db_path = config["paths"]["database"]

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {db_path}")


def insert_customers(df):
    conn = get_connection()

    cols = [
        "customer_id", "contract_type", "tenure_months",
        "monthly_charges", "tenure_segment"
    ]

    # Keep only available columns
    available = [c for c in cols if c in df.columns]
    df_insert = df[available].copy()

    df_insert.to_sql("customers", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Inserted {len(df_insert)} rows into customers")


def insert_predictions(df):
    conn = get_connection()

    cols = [
        "customer_id", "churn_probability", "risk_tier", "churn_predicted"
    ]

    available = [c for c in cols if c in df.columns]
    df_insert = df[available].copy()

    df_insert.to_sql("churn_predictions", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Inserted {len(df_insert)} rows into churn_predictions")


def insert_business_summary(df):
    conn = get_connection()

    cols = [
        "customer_id", "expected_remaining_months", "future_revenue_loss",
        "revenue_at_risk", "retention_cost", "net_retention_value",
        "retention_roi", "priority_score", "is_worth_retaining",
        "retention_action", "urgency", "contact_channel"
    ]

    available = [c for c in cols if c in df.columns]
    df_insert = df[available].copy()

    df_insert.to_sql("business_summary", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Inserted {len(df_insert)} rows into business_summary")


def run_query(sql):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def run_query_file(filepath):
    with open(filepath, "r") as f:
        sql = f.read()
    return run_query(sql)