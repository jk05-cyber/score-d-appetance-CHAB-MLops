"""Simple data validation routines."""
import pandas as pd
from typing import Dict, Any


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> Dict[str, Any]:
    """Check basic properties of a dataframe."""
    report = {}
    report["columns_present"] = all(col in df.columns for col in required_columns)
    report["missing_columns"] = [col for col in required_columns if col not in df.columns]
    report["num_rows"] = len(df)
    report["num_duplicates"] = df.duplicated().sum()
    report["missing_values_ratio"] = df.isna().mean().to_dict()
    report["dtypes"] = df.dtypes.apply(lambda x: str(x)).to_dict()
    return report


def validate_all(rc: pd.DataFrame, pc: pd.DataFrame, mv: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Produce a report for each of the three tables."""
    from ..config import settings

    return {
        "RC": validate_dataframe(rc, settings.REQUIRED_COLUMNS.get("RC", [])),
        "PC": validate_dataframe(pc, settings.REQUIRED_COLUMNS.get("PC", [])),
        "MOUVEMENT": validate_dataframe(mv, settings.REQUIRED_COLUMNS.get("MOUVEMENT", [])),
    }
