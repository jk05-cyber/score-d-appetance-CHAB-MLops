"""Prediction helper for saved models."""
import mlflow
import pandas as pd


def load_model(model_path: str = None):
    """Load a model from MLflow or local path."""
    if model_path is None:
        # assume latest run
        model_path = "models:/logreg/latest"
    return mlflow.sklearn.load_model(model_path)


def predict(df: pd.DataFrame, model=None) -> pd.DataFrame:
    """Return score, probability, class for each client row."""
    if model is None:
        model = load_model()
    proba = model.predict_proba(df)[:, 1]
    return pd.DataFrame({
        "score": proba,
        "probability": proba,
        "prediction": (proba >= 0.5).astype(int)
    }, index=df.index)
