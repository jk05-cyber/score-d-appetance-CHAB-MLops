"""Transaction-level feature engineering."""
import pandas as pd


def add_mouvement_features(mv: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction history to client-level indicators."""
    df = mv.copy()
    grp = df.groupby("client_id")
    features = pd.DataFrame({
        "sum_amount": grp["amount"].sum(),
        "mean_amount": grp["amount"].mean(),
        "std_amount": grp["amount"].std().fillna(0),
        "n_transactions": grp.size(),
    }).reset_index()
    # cashflow net (positive minus negative)
    pos = df[df.amount > 0].groupby("client_id")["amount"].sum()
    neg = df[df.amount < 0].groupby("client_id")["amount"].sum()
    features["net_flow"] = features["client_id"].map(pos).fillna(0) + features["client_id"].map(neg).fillna(0)
    return features
