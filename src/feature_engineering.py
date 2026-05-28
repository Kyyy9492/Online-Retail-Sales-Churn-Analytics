import pandas as pd


def add_basic_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add revenue, cancellation flag, and calendar features."""
    out = df.copy()
    out["revenue"] = out["quantity"] * out["unit_price"]
    out["is_cancelled"] = out["invoice_no"].astype(str).str.startswith("C") | (out["quantity"] < 0)
    out["invoice_month"] = pd.to_datetime(out["invoice_date"]).dt.to_period("M").astype(str)
    return out


def make_customer_features(sales_customer: pd.DataFrame) -> pd.DataFrame:
    """Create customer-level features for churn and RFM analysis."""
    snapshot_date = sales_customer["invoice_date"].max() + pd.Timedelta(days=1)
    features = sales_customer.groupby("customer_id").agg(
        first_purchase_date=("invoice_date", "min"),
        last_purchase_date=("invoice_date", "max"),
        recency_days=("invoice_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("invoice_no", "nunique"),
        monetary_value=("revenue", "sum"),
        unique_products=("stock_code", "nunique"),
        active_months=("invoice_month", "nunique"),
    ).reset_index()
    features["avg_order_value"] = features["monetary_value"] / features["frequency"]
    features["customer_lifetime_days"] = (features["last_purchase_date"] - features["first_purchase_date"]).dt.days
    return features
