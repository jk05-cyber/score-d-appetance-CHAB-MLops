import pandas as pd
from src.models.train import train_models


def test_train_runs(tmp_path, monkeypatch):
    # create a tiny dataset with target
    df = pd.DataFrame({
        "client_id": [1,2,3,4],
        "age": [30,40,50,60],
        "sum_amount": [100,200,300,400],
        "n_products": [1,2,1,3],
        "chab_target": [0,1,0,1]
    })
    results = train_models(df)
    assert "best" in results
    assert results["best"]["test_auc"] >= 0
