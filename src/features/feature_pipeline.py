"""Wrapper to run all feature modules and produce a single table."""
import pandas as pd
from typing import Tuple

from .rc_features import add_rc_features
from .pc_features import add_pc_features
from .mouvement_features import add_mouvement_features


def create_feature_set(rc: pd.DataFrame, pc: pd.DataFrame, mv: pd.DataFrame) -> pd.DataFrame:
    """Generate joined feature set from raw tables.

    Returns a dataframe keyed by client_id with all engineered features.
    """
    rc_feat = add_rc_features(rc)
    pc_feat = add_pc_features(pc)
    mv_feat = add_mouvement_features(mv)

    # start with rc, then merge other sets
    df = rc_feat.merge(pc_feat, on="ID_CLIENT", how="left")
    df = df.merge(mv_feat, on="ID_CLIENT", how="left")
    return df


def prepare_for_model(df: pd.DataFrame, target: pd.Series = None) -> Tuple[pd.DataFrame, pd.Series]:
    """Returns X, y suitable for sklearn. Drops identifier columns."""
    X = df.copy()
    if target is not None:
        X["target"] = target
    y = None
    if "target" in X.columns:
        y = X.pop("target")
    X = X.drop(columns=[col for col in X.columns if col == "ID_CLIENT" or "date" in col.lower()])
    # One-hot encode categorical columns
    X = pd.get_dummies(X, drop_first=True)
    return X, y
