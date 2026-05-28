# Dashboard Build Guide

## Page 1: Executive Overview

Recommended visuals:

- KPI cards: total revenue, orders, active customers, average order value, churn risk rate
- Line chart: monthly revenue trend
- Bar chart: top countries by revenue
- Bar chart: top products by revenue

Recommended data files:

- `data/processed/monthly_sales_summary.csv`
- `data/processed/country_performance.csv`
- `data/processed/product_performance_top200.csv`

## Page 2: Customer Segmentation

Recommended visuals:

- Donut/bar chart: customer count by RFM segment
- Bar chart: revenue by RFM segment
- Table: segment summary
- Scatter plot: recency vs monetary value

Recommended data files:

- `data/processed/customer_rfm_segments.csv`
- `data/processed/segment_summary.csv`

## Page 3: Churn Risk

Recommended visuals:

- KPI card: churn risk rate
- Bar chart: churn risk by segment
- Table: top high-value churn-risk customers
- Bar chart: revenue at risk by segment

Recommended data files:

- `data/processed/customer_churn_labels.csv`
- `data/processed/high_value_churn_risk_customers.csv`

## Page 4: Retention

Recommended visuals:

- Matrix heatmap: cohort retention matrix
- Line chart: active customers over time
- Bar chart: repeat purchase behavior

Recommended data files:

- `data/processed/cohort_retention_matrix.csv`
- `data/processed/monthly_sales_summary.csv`

## Suggested Dashboard Title

**Online Retail Sales & Customer Churn Analytics Dashboard**
