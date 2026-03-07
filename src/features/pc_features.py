"""Features derived from products and accounts."""
import pandas as pd


def add_pc_features(pc: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregates per client."""
    df = pc.copy()
    # number of distinct product types
    agg = df.groupby("client_id")["product_type"].nunique().reset_index(name="n_products")
    # earliest and latest opened
    dates = df.groupby("client_id")["opened_date"].agg(["min", "max"]).reset_index()
    dates.columns = ["client_id", "first_prod_date", "last_prod_date"]
    result = agg.merge(dates, on="client_id", how="left")
    return result
