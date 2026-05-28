-- Monthly sales KPI template

SELECT
    DATE_TRUNC('month', invoice_date) AS invoice_month,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    SUM(revenue) AS total_revenue,
    SUM(revenue) / COUNT(DISTINCT invoice_no) AS avg_order_value
FROM transactions_clean
WHERE is_cancelled = 0
GROUP BY 1
ORDER BY 1;
