"""Transaction-level feature engineering."""
import pandas as pd


def add_mouvement_features(mv: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction history to client-level indicators."""
    df = mv.copy()
    grp = df.groupby("ID_CLIENT")
    features = pd.DataFrame({
        "sum_amount": grp["MONTANT"].sum(),
        "mean_amount": grp["MONTANT"].mean(),
        "std_amount": grp["MONTANT"].std().fillna(0),
        "n_transactions": grp.size(),
    }).reset_index()
    # cashflow net (positive minus negative)
    pos = df[df.MONTANT > 0].groupby("ID_CLIENT")["MONTANT"].sum()
    neg = df[df.MONTANT < 0].groupby("ID_CLIENT")["MONTANT"].sum()
    features["net_flow"] = features["ID_CLIENT"].map(pos).fillna(0) + features["ID_CLIENT"].map(neg).fillna(0)
    return features
