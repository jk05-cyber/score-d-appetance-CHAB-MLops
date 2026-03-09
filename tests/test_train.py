import pandas as pd
from src.models.train import train_models


def test_train_runs(tmp_path, monkeypatch):
    # create a larger dataset with target
    import numpy as np
    np.random.seed(42)
    n_samples = 100
    df = pd.DataFrame({
        "ID_CLIENT": range(1, n_samples + 1),
        "AGE": np.random.randint(20, 80, n_samples),
        "tenure_days": np.random.randint(100, 3000, n_samples),
        "n_products": np.random.randint(1, 5, n_samples),
        "sum_amount": np.random.rand(n_samples) * 10000,
        "mean_amount": np.random.rand(n_samples) * 5000,
        "std_amount": np.random.rand(n_samples) * 2000,
        "n_transactions": np.random.randint(1, 50, n_samples),
        "net_flow": np.random.rand(n_samples) * 5000 - 2500,
        "chab_target": np.random.randint(0, 2, n_samples)
    })
    results = train_models(df)
    assert "best" in results
    assert results["best"]["test_auc"] >= 0
