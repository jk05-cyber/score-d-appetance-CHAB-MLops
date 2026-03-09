"""Assembly of the modelling dataset."""
import pandas as pd
from typing import Tuple

from .load_data import load_rc, load_pc, load_mouvement
from ..config import settings


def construct_target(rc: pd.DataFrame, pc: pd.DataFrame, mv: pd.DataFrame) -> pd.Series:
    """Define a simple target: client opened a habitat loan in PC within last year.

    Hypothesis: any product type 'CREDIT_CONSO' opened within the last 365 days indicates
    a positive label. This is illustrative; in real life, business rules would be
    far more complex.
    """
    import numpy as np
    reference = pd.Timestamp.today()
    pc = pc.copy()
    pc["recent_habitat"] = ((pc["TYPE_PRODUIT"] == "CREDIT_CONSO") &
                              ((reference - pc["DATE_SOUSCRIPTION"]).dt.days <= 365))
    flagged = pc.loc[pc["recent_habitat"], settings.ID_COL].unique()
    return rc[settings.ID_COL].isin(flagged).astype(int)


def build_dataset(save_path: str = None) -> pd.DataFrame:
    """Load raw data, merge, create features and target, and persist processed dataset."""
    rc = load_rc()
    pc = load_pc()
    mv = load_mouvement()

    # basic merge on client id
    df = rc.merge(pc.groupby(settings.ID_COL)["TYPE_PRODUIT"].nunique().reset_index(
        name="n_products"), on=settings.ID_COL, how="left")
    df = df.merge(mv.groupby(settings.ID_COL)["MONTANT"].sum().reset_index(
        name="total_amount"), on=settings.ID_COL, how="left")

    # target
    df[settings.TARGET_COLUMN] = construct_target(rc, pc, mv)

    # save
    path = save_path or (settings.PROCESSED_DIR / "dataset.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_processed(path: str = None) -> pd.DataFrame:
    """Utility to read the processed dataset."""
    path = path or (settings.PROCESSED_DIR / "dataset.csv")
    return pd.read_csv(path)
