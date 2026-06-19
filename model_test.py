from joblib import load
import pandas as pd

model = load("models/champion_xgboost.joblib")

preprocessor = model.named_steps["preprocessor"]
xgb_model = model.named_steps["model"]

feature_names = preprocessor.get_feature_names_out()

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": xgb_model.feature_importances_
})

print(
    importance_df
    .sort_values("Importance", ascending=False)
    .head(30)
)