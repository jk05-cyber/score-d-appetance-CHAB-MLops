"""Evaluation utilities."""
import matplotlib.pyplot as plt
from sklearn.metrics import (roc_auc_score, average_precision_score,
                             f1_score, precision_score, recall_score)


def evaluate(y_true, y_proba, output_path=None) -> dict:
    """Compute common metrics and optionally save a simple plot."""
    results = {}
    results["roc_auc"] = roc_auc_score(y_true, y_proba)
    results["pr_auc"] = average_precision_score(y_true, y_proba)
    threshold = 0.5
    y_pred = (y_proba >= threshold).astype(int)
    results["f1"] = f1_score(y_true, y_pred)
    results["precision"] = precision_score(y_true, y_pred)
    results["recall"] = recall_score(y_true, y_pred)

    if output_path:
        plt.figure()
        plt.hist(y_proba[y_true == 0], bins=50, alpha=0.5, label="neg")
        plt.hist(y_proba[y_true == 1], bins=50, alpha=0.5, label="pos")
        plt.legend()
        plt.title("Score distribution")
        plt.savefig(output_path)
    return results
