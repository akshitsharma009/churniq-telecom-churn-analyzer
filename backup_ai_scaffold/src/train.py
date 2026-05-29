# ChurnIQ - train.py
# Model training, comparison, and selection

import pandas as pd
import numpy as np
import pickle
import yaml
import os
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE

from src.features import get_model_features


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def prepare_data(df):
    config = load_config()
    target = config["model"]["target"]
    features = get_model_features()

    df = df.copy()

    # Encode tenure_segment
    le = LabelEncoder()
    df["tenure_segment"] = le.fit_transform(df["tenure_segment"].astype(str))

    X = df[features]
    y = df[target]

    return X, y, le


def split_data(X, y):
    config = load_config()
    test_size = config["model"]["test_size"]
    val_size = config["model"]["val_size"]
    random_state = config["model"]["random_state"]

    # First split: train+val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Second split: train vs val
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=random_state, stratify=y_temp
    )

    print(f"✅ Train: {X_train.shape[0]} | Val: {X_val.shape[0]} | Test: {X_test.shape[0]}")
    return X_train, X_val, X_test, y_train, y_val, y_test


def apply_smote(X_train, y_train):
    config = load_config()
    random_state = config["model"]["random_state"]
    smote = SMOTE(random_state=random_state)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    print(f"✅ SMOTE applied — Train size: {X_resampled.shape[0]}")
    return X_resampled, y_resampled


def get_models():
    config = load_config()
    rs = config["model"]["random_state"]

    return {
        "RandomForest": RandomForestClassifier(
            n_estimators=100, random_state=rs, n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, random_state=rs,
            eval_metric="logloss", verbosity=0
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=100, random_state=rs,
            verbose=-1
        ),
        "CatBoost": CatBoostClassifier(
            iterations=100, random_state=rs,
            verbose=0
        )
    }


def train_and_compare(X_train, y_train, X_val, y_val):
    config = load_config()
    cv_folds = config["model"]["cv_folds"]
    random_state = config["model"]["random_state"]

    models = get_models()
    results = {}

    mlflow.set_experiment("ChurnIQ")

    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            # CV on training data
            cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="f1_macro")

            # Train on full training data
            model.fit(X_train, y_train)

            # Validate
            val_preds = model.predict(X_val)
            val_f1 = f1_score(y_val, val_preds, average="macro")

            results[name] = {
                "model": model,
                "cv_f1_mean": cv_scores.mean(),
                "cv_f1_std": cv_scores.std(),
                "val_f1": val_f1
            }

            mlflow.log_param("model", name)
            mlflow.log_metric("cv_f1_mean", cv_scores.mean())
            mlflow.log_metric("cv_f1_std", cv_scores.std())
            mlflow.log_metric("val_f1", val_f1)

            print(f"✅ {name} — CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f} | Val F1: {val_f1:.4f}")

    # Select best model by val_f1
    best_name = max(results, key=lambda k: results[k]["val_f1"])
    best_model = results[best_name]["model"]
    print(f"\n🏆 Best Model: {best_name} (Val F1: {results[best_name]['val_f1']:.4f})")

    return best_name, best_model, results


def save_model(model, label_encoder):
    config = load_config()
    model_path = os.path.join(config["paths"]["models"], "best_model.pkl")
    le_path = os.path.join(config["paths"]["models"], "feature_pipeline.pkl")

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    with open(le_path, "wb") as f:
        pickle.dump(label_encoder, f)

    print(f"✅ Model saved: {model_path}")
    print(f"✅ Pipeline saved: {le_path}")