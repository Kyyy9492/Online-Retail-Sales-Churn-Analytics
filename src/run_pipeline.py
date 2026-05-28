from pathlib import Path
import pandas as pd
import numpy as np

RAW_PATH = Path("data/raw/online_retail_II.xlsx")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_online_retail(path: Path = RAW_PATH) -> pd.DataFrame:
    xl = pd.ExcelFile(path)
    frames = []
    for sheet in xl.sheet_names:
        temp = pd.read_excel(path, sheet_name=sheet)
        temp["source_sheet"] = sheet
        frames.append(temp)
    return pd.concat(frames, ignore_index=True)


def clean_transactions(raw: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Invoice": "invoice_no", "StockCode": "stock_code", "Description": "description",
        "Quantity": "quantity", "InvoiceDate": "invoice_date", "Price": "unit_price",
        "Customer ID": "customer_id", "Country": "country",
    }
    df = raw.rename(columns=rename_map).copy()
    df["invoice_no"] = df["invoice_no"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    df["description"] = df["description"].astype(str).str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["is_cancelled"] = df["invoice_no"].str.startswith("C") | (df["quantity"] < 0)
    df["invoice_month"] = df["invoice_date"].dt.to_period("M").astype(str)
    return df


def build_sales_outputs(df: pd.DataFrame) -> None:
    sales = df[(~df["is_cancelled"]) & (df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    monthly_sales = sales.groupby("invoice_month").agg(
        total_revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        active_customers=("customer_id", lambda x: x.nunique(dropna=True)),
        units_sold=("quantity", "sum")
    ).reset_index()
    monthly_sales["avg_order_value"] = monthly_sales["total_revenue"] / monthly_sales["orders"]

    country_performance = sales.groupby("country").agg(
        total_revenue=("revenue", "sum"), orders=("invoice_no", "nunique"),
        customers=("customer_id", lambda x: x.nunique(dropna=True)), units_sold=("quantity", "sum")
    ).reset_index().sort_values("total_revenue", ascending=False)
    country_performance["avg_order_value"] = country_performance["total_revenue"] / country_performance["orders"]

    product_performance = sales.groupby(["stock_code", "description"]).agg(
        total_revenue=("revenue", "sum"), units_sold=("quantity", "sum"),
        orders=("invoice_no", "nunique"), customers=("customer_id", lambda x: x.nunique(dropna=True))
    ).reset_index().sort_values("total_revenue", ascending=False)

    monthly_sales.to_csv(PROCESSED_DIR / "monthly_sales_summary.csv", index=False)
    country_performance.to_csv(PROCESSED_DIR / "country_performance.csv", index=False)
    product_performance.head(200).to_csv(PROCESSED_DIR / "product_performance_top200.csv", index=False)


def build_rfm_churn_outputs(df: pd.DataFrame, churn_days: int = 90) -> None:
    sales_customer = df[(~df["is_cancelled"]) & (df["quantity"] > 0) & (df["unit_price"] > 0) & df["customer_id"].notna()].copy()
    sales_customer["customer_id"] = sales_customer["customer_id"].astype(int).astype(str)
    snapshot_date = sales_customer["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = sales_customer.groupby("customer_id").agg(
        first_purchase_date=("invoice_date", "min"),
        last_purchase_date=("invoice_date", "max"),
        recency_days=("invoice_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("invoice_no", "nunique"),
        monetary_value=("revenue", "sum"),
        unique_products=("stock_code", "nunique"),
        active_months=("invoice_month", "nunique")
    ).reset_index()
    rfm["avg_order_value"] = rfm["monetary_value"] / rfm["frequency"]
    rfm["customer_lifetime_days"] = (rfm["last_purchase_date"] - rfm["first_purchase_date"]).dt.days

    rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary_value"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["rfm_score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

    def assign_segment(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        if r >= 4 and f >= 4 and m >= 4: return "Champions"
        if r >= 3 and f >= 4: return "Loyal Customers"
        if r >= 4 and f <= 2: return "New / Promising"
        if r <= 2 and f >= 4 and m >= 4: return "Cannot Lose Them"
        if r <= 2 and (f >= 3 or m >= 3): return "At Risk"
        if r == 3 and f >= 3: return "Need Attention"
        if r <= 2 and f <= 2: return "Hibernating / Lost"
        return "Potential Loyalists"

    rfm["customer_segment"] = rfm.apply(assign_segment, axis=1)
    rfm["churn_risk_label"] = (rfm["recency_days"] > churn_days).astype(int)
    rfm["churn_status"] = np.where(rfm["churn_risk_label"] == 1, "Inactive / Churn Risk", "Active")

    segment_summary = rfm.groupby("customer_segment").agg(
        customers=("customer_id", "nunique"), revenue=("monetary_value", "sum"),
        avg_recency_days=("recency_days", "mean"), avg_frequency=("frequency", "mean"),
        avg_monetary_value=("monetary_value", "mean"), churn_risk_rate=("churn_risk_label", "mean")
    ).reset_index().sort_values("revenue", ascending=False)

    rfm.to_csv(PROCESSED_DIR / "customer_rfm_segments.csv", index=False)
    segment_summary.to_csv(PROCESSED_DIR / "segment_summary.csv", index=False)
    rfm[rfm["churn_risk_label"] == 1].sort_values("monetary_value", ascending=False).head(100).to_csv(
        PROCESSED_DIR / "high_value_churn_risk_customers.csv", index=False
    )


def main():
    raw = load_online_retail()
    df = clean_transactions(raw)
    build_sales_outputs(df)
    build_rfm_churn_outputs(df)
    print("Pipeline completed. Processed CSVs saved to data/processed/.")


if __name__ == "__main__":
    main()
