"""Generate a simple drift report comparing train vs new scored data."""
import pandas as pd
from ..config import settings


def drift_metrics(train_df: pd.DataFrame, scored_df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-column distribution differences (simple KS statistic).
    Only compares columns that exist in both dataframes.
    """
    from scipy.stats import ks_2samp
    # Find common numeric columns
    common_cols = set(train_df.columns) & set(scored_df.columns)
    numeric_cols = [c for c in common_cols if train_df[c].dtype.kind in "bifc" and scored_df[c].dtype.kind in "bifc"]
    
    records = []
    for c in numeric_cols:
        try:
            stat, p = ks_2samp(train_df[c].dropna(), scored_df[c].dropna())
            records.append({"feature": c, "ks_stat": stat, "p_value": p})
        except Exception as e:
            # Skip features with issues
            pass
    return pd.DataFrame(records) if records else pd.DataFrame(columns=["feature", "ks_stat", "p_value"])


def generate_report(train_path: str, scored_path: str, output: str = None):
    train = pd.read_csv(train_path)
    scored = pd.read_csv(scored_path)
    report = drift_metrics(train, scored)
    if output:
        report.to_csv(output, index=False)
    return report
