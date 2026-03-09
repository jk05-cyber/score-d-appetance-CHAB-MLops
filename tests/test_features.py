import pandas as pd
from src.features.rc_features import add_rc_features
from src.features.pc_features import add_pc_features
from src.features.mouvement_features import add_mouvement_features


def test_rc_features():
    df = pd.DataFrame({
        "ID_CLIENT": [1],
        "DATE_ENTREE_BANQUE": pd.to_datetime(["2020-01-01"]),
        "AGE": [43],
        "SITUATION_FAMILIALE": ["employee"],
    })
    out = add_rc_features(df)
    assert "tenure_days" in out.columns


def test_pc_features():
    df = pd.DataFrame({
        "ID_CLIENT": [1, 1],
        "TYPE_PRODUIT": ["a", "b"],
        "DATE_SOUSCRIPTION": pd.to_datetime(["2021-01-01", "2022-01-01"]),
    })
    out = add_pc_features(df)
    assert out.loc[0, "n_products"] == 2


def test_mouvement_features():
    df = pd.DataFrame({
        "ID_CLIENT": [1, 1, 2],
        "MONTANT": [100.0, -50.0, 200.0],
    })
    out = add_mouvement_features(df)
    assert "net_flow" in out.columns
