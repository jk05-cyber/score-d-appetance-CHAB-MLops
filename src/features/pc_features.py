"""Features derived from products and accounts."""
import pandas as pd


def add_pc_features(pc: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregates per client."""
    df = pc.copy()
    # number of distinct product types
    agg = df.groupby("ID_CLIENT")["TYPE_PRODUIT"].nunique().reset_index(name="n_products")
    # earliest and latest opened
    dates = df.groupby("ID_CLIENT")["DATE_SOUSCRIPTION"].agg(["min", "max"]).reset_index()
    dates.columns = ["ID_CLIENT", "first_prod_date", "last_prod_date"]
    result = agg.merge(dates, on="ID_CLIENT", how="left")
    return result
