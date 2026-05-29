# ChurnIQ - preprocess.py
# Data loading, cleaning, and preparation

import pandas as pd
import numpy as np
import yaml
import os


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_data(path=None):
    config = load_config()
    if path is None:
        path = config["paths"]["raw_data"]
    df = pd.read_csv(path)
    print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def clean_data(df):
    df = df.copy()

    # Lowercase column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"✅ Duplicates removed: {before - len(df)}")

    # Target column — map to binary
    if "churn" in df.columns:
        df["churn"] = df["churn"].map({"Yes": 1, "No": 0, 1: 1, 0: 0})

    # Separate numeric and categorical
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Fill missing — numeric with median, categorical with mode
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print(f"✅ Missing values handled")
    print(f"✅ Clean data shape: {df.shape}")

    return df


def save_processed(df, filename="train_cleaned.csv"):
    config = load_config()
    out_path = os.path.join(config["paths"]["processed_data"], filename)
    df.to_csv(out_path, index=False)
    print(f"✅ Saved: {out_path}")