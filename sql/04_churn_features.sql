-- Customer churn feature template
-- Churn is defined as no purchase in the last 90 days before the snapshot date.

WITH customer_features AS (
    SELECT
        customer_id,
        MIN(invoice_date) AS first_purchase_date,
        MAX(invoice_date) AS last_purchase_date,
        DATE_DIFF('day', MAX(invoice_date), DATE '2011-12-10') AS recency_days,
        COUNT(DISTINCT invoice_no) AS frequency,
        SUM(revenue) AS monetary_value,
        COUNT(DISTINCT stock_code) AS unique_products
    FROM transactions_clean
    WHERE is_cancelled = 0
      AND customer_id IS NOT NULL
    GROUP BY customer_id
)
SELECT
    *,
    monetary_value / NULLIF(frequency, 0) AS avg_order_value,
    CASE WHEN recency_days > 90 THEN 1 ELSE 0 END AS churn_risk_label
FROM customer_features;
