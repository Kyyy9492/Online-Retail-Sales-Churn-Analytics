-- Customer RFM template

SELECT
    customer_id,
    DATE_DIFF('day', MAX(invoice_date), DATE '2011-12-10') AS recency_days,
    COUNT(DISTINCT invoice_no) AS frequency,
    SUM(revenue) AS monetary_value
FROM transactions_clean
WHERE is_cancelled = 0
GROUP BY customer_id;
