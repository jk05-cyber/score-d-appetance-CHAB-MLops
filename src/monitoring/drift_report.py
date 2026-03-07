"""Generate a simple drift report comparing train vs new scored data."""
import pandas as pd
from ..config import settings


def drift_metrics(train_df: pd.DataFrame, scored_df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-column distribution differences (simple KS statistic)."""
    from scipy.stats import ks_2samp
    cols = [c for c in train_df.columns if train_df[c].dtype.kind in "bifc"]
    records = []
    for c in cols:
        stat, p = ks_2samp(train_df[c].dropna(), scored_df[c].dropna())
        records.append({"feature": c, "ks_stat": stat, "p_value": p})
    return pd.DataFrame(records)


def generate_report(train_path: str, scored_path: str, output: str = None):
    train = pd.read_csv(train_path)
    scored = pd.read_csv(scored_path)
    report = drift_metrics(train, scored)
    if output:
        report.to_csv(output, index=False)
    return report
