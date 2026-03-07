import pandas as pd
from src.features.rc_features import add_rc_features
from src.features.pc_features import add_pc_features
from src.features.mouvement_features import add_mouvement_features


def test_rc_features():
    df = pd.DataFrame({
        "client_id": [1],
        "date_opened": ["2020-01-01"],
        "birthdate": ["1980-06-15"],
        "situation": ["employee"],
    })
    out = add_rc_features(df)
    assert "age" in out.columns
    assert out["socio_pro_idx"].iloc[0] == 0


def test_pc_features():
    df = pd.DataFrame({
        "client_id": [1, 1],
        "product_type": ["a", "b"],
        "opened_date": ["2021-01-01", "2022-01-01"],
    })
    out = add_pc_features(df)
    assert out.loc[0, "n_products"] == 2


def test_mouvement_features():
    df = pd.DataFrame({
        "client_id": [1, 1, 2],
        "amount": [100, -50, 200],
    })
    out = add_mouvement_features(df)
    assert "net_flow" in out.columns
