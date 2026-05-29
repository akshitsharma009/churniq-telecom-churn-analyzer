# ChurnIQ - evaluate.py
# Model evaluation metrics and reporting

import pandas as pd
import numpy as np
import pickle
import yaml
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    f1_score, roc_auc_score, precision_score,
    recall_score, confusion_matrix, classification_report
)


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_model():
    config = load_config()
    model_path = os.path.join(config["paths"]["models"], "best_model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "f1_macro":  f1_score(y_test, y_pred, average="macro"),
        "f1_binary": f1_score(y_test, y_pred, average="binary"),
        "roc_auc":   roc_auc_score(y_test, y_prob),
        "precision": precision_score(y_test, y_pred),
        "recall":    recall_score(y_test, y_pred),
    }

    print("\n📊 Model Evaluation Results")
    print("=" * 40)
    for k, v in metrics.items():
        print(f"  {k:<15}: {v:.4f}")
    print("=" * 40)
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))

    return metrics, y_pred, y_prob


def plot_confusion_matrix(y_test, y_pred, save=True):
    config = load_config()
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=["No Churn", "Churn"],
        yticklabels=["No Churn", "Churn"]
    )
    plt.title("Confusion Matrix — ChurnIQ")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()

    if save:
        path = os.path.join(config["paths"]["reports"], "figures", "confusion_matrix.png")
        plt.savefig(path)
        print(f"✅ Saved: {path}")

    plt.show()


def plot_roc_curve(model, X_test, y_test, save=True):
    from sklearn.metrics import roc_curve
    config = load_config()

    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color="royalblue", lw=2, label=f"ROC Curve (AUC = {auc:.4f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve — ChurnIQ")
    plt.legend(loc="lower right")
    plt.tight_layout()

    if save:
        path = os.path.join(config["paths"]["reports"], "figures", "roc_curve.png")
        plt.savefig(path)
        print(f"✅ Saved: {path}")

    plt.show()


def save_metrics_report(metrics, model_name="Best Model"):
    config = load_config()
    report_path = os.path.join(config["paths"]["reports"], "model_performance.md")

    with open(report_path, "w") as f:
        f.write(f"# ChurnIQ — Model Performance Report\n\n")
        f.write(f"## Model: {model_name}\n\n")
        f.write("| Metric | Score |\n")
        f.write("|--------|-------|\n")
        for k, v in metrics.items():
            f.write(f"| {k} | {v:.4f} |\n")

    print(f"✅ Report saved: {report_path}")