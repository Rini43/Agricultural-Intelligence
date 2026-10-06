import joblib
import pandas as pd
import shap


model = joblib.load(
    "models/best_model.pkl"
)


def explain_prediction(data):

    # Get preprocessing pipeline
    preprocessor = model.named_steps[
        "preprocessor"
    ]

    xgb_model = model.named_steps[
        "model"
    ]

    transformed = preprocessor.transform(
        data
    )

    # Feature names
    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    # SHAP explainer
    explainer = shap.TreeExplainer(
        xgb_model
    )

    shap_values = explainer.shap_values(
        transformed
    )

    return (
        shap_values,
        feature_names
    )

