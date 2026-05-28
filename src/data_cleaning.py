"""
Data cleaning functions for Online Retail II project.
"""

import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Invoice": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "Price": "unit_price",
        "Customer ID": "customer_id",
        "Country": "country",
    }
    return df.rename(columns=rename_map)


def add_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["is_cancelled"] = (
        df["invoice_no"].astype(str).str.startswith("C") | (df["quantity"] < 0)
    )
    df["invoice_month"] = df["invoice_date"].dt.to_period("M").astype(str)
    return df
