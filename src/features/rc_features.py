"""Feature generation from the client reference table."""
import pandas as pd


def add_rc_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple demographic and profile features.

    - age: from birthdate if present, otherwise use age column
    - tenure: days since account opened
    - socio_pro: one-hot encode situation
    """
    df = df.copy()
    today = pd.Timestamp.today()
    if "birthdate" in df.columns:
        df["age"] = (today - pd.to_datetime(df["birthdate"])).dt.days // 365
    df["tenure_days"] = (today - pd.to_datetime(df.get("date_opened", today))).dt.days

    # examples of categorical
    socio_map = {"employee": 0, "self_employed": 1, "retired": 2, "unemployed": 3}
    if "situation" in df.columns:
        df["socio_pro_idx"] = df["situation"].map(socio_map).fillna(-1)
    return df
