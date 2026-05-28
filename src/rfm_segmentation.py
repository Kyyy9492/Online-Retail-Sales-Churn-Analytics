"""
RFM segmentation helper functions.
"""

import pandas as pd


def build_rfm_table(df: pd.DataFrame, snapshot_date=None) -> pd.DataFrame:
    valid = df[(df["is_cancelled"] == False) & df["customer_id"].notna()].copy()

    if snapshot_date is None:
        snapshot_date = valid["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = valid.groupby("customer_id").agg(
        recency_days=("invoice_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("invoice_no", "nunique"),
        monetary_value=("revenue", "sum"),
    ).reset_index()

    return rfm
