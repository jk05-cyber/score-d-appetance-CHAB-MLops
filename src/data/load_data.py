"""Data loading utilities for the credit habitat project."""
import pandas as pd
from typing import Tuple

from ..config import settings


def _read_csv(path: str, **kwargs) -> pd.DataFrame:
    """Helper for reading CSV with common defaults."""
    return pd.read_csv(path, encoding=kwargs.get("encoding", "utf-8"), sep=kwargs.get("sep", ","),
                       parse_dates=kwargs.get("parse_dates", []), dtype=kwargs.get("dtype", {}))


def load_rc(path: str = None) -> pd.DataFrame:
    """Load the RC (client reference) table."""
    path = path or settings.RC_FILE
    df = _read_csv(path, parse_dates=["DATE_ENTREE_BANQUE"])
    return df


def load_pc(path: str = None) -> pd.DataFrame:
    """Load product/comptes information."""
    path = path or settings.PC_FILE
    df = _read_csv(path, parse_dates=["DATE_SOUSCRIPTION"])
    return df


def load_mouvement(path: str = None) -> pd.DataFrame:
    """Load movement/transaction history."""
    path = path or settings.MOUVEMENT_FILE
    df = _read_csv(path, parse_dates=["DATE_OPERATION"])
    return df


def load_all() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all three raw tables and return them."""
    return load_rc(), load_pc(), load_mouvement()
