"""Model training routines."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import mlflow

from ..config import settings
from ..data.build_dataset import load_processed
from ..features.feature_pipeline import prepare_for_model


def train_models(df: pd.DataFrame = None) -> dict:
    """Train baseline and advanced models, return metrics and model objects."""
    if df is None:
        df = load_processed()
    X, y = prepare_for_model(df.drop(columns=[settings.TARGET_COLUMN]), df[settings.TARGET_COLUMN])
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=settings.TEST_SIZE + settings.VALIDATION_SIZE,
        random_state=settings.RANDOM_STATE, stratify=y)
    val_relative = settings.VALIDATION_SIZE / (settings.TEST_SIZE + settings.VALIDATION_SIZE)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=val_relative, random_state=settings.RANDOM_STATE, stratify=y_temp)

    results = {}
    for name, model in [
        ("logreg", LogisticRegression(max_iter=1000, random_state=settings.RANDOM_STATE)),
        ("rf", RandomForestClassifier(n_estimators=100, random_state=settings.RANDOM_STATE))
    ]:
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", model)
        ])
        with mlflow.start_run(run_name=name):
            pipe.fit(X_train, y_train)
            y_pred = pipe.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, y_pred)
            mlflow.log_metric("val_auc", auc)
            mlflow.sklearn.log_model(pipe, name)
        results[name] = {"model": pipe, "val_auc": auc}

    # select best
    best = max(results.items(), key=lambda x: x[1]["val_auc"])
    best_name, best_info = best
    with mlflow.start_run(run_name="final_evaluate"):
        y_test_pred = best_info["model"].predict_proba(X_test)[:, 1]
        test_auc = roc_auc_score(y_test, y_test_pred)
        mlflow.log_metric("test_auc", test_auc)
    results["best"] = {"name": best_name, "info": best_info, "test_auc": test_auc}
    return results


def main():
    df = load_processed()
    return train_models(df)


if __name__ == "__main__":
    train_models()
