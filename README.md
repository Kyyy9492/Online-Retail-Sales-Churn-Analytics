# Online Retail Sales & Customer Churn Analytics

## Project Overview

This project analyzes transaction-level online retail data to understand sales performance, customer value, product demand, and churn risk. The dataset contains two yearly worksheets, **2009–2010** and **2010–2011**, with more than one million invoice-line records.

The final deliverables are designed to demonstrate a practical data analyst workflow:

- Data cleaning and transaction validation
- Sales KPI analysis
- Customer segmentation using RFM
- Churn / inactive-customer risk labeling
- Cohort retention analysis
- Market and product performance analysis
- Dashboard-ready output tables
- Optional predictive modeling for churn risk

## Dataset

**Source file:** `online_retail_II.xlsx`

Expected columns:

| Column | Description |
|---|---|
| Invoice | Invoice ID; cancellation invoices usually start with `C` |
| StockCode | Product code |
| Description | Product description |
| Quantity | Quantity purchased or returned |
| InvoiceDate | Transaction timestamp |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer country |

The workbook contains two sheets:

| Sheet | Approximate Rows | Columns |
|---|---:|---:|
| Year 2009-2010 | 525,461 | 8 |
| Year 2010-2011 | 541,910 | 8 |

## Business Questions

This project answers the following business questions:

1. **Sales Performance**
   - What are the monthly revenue, order volume, and average order value trends?
   - Which countries contribute the most revenue?
   - Which products drive the most sales?

2. **Customer Value**
   - Who are the highest-value customers?
   - How are customers distributed by recency, frequency, and monetary value?
   - Which customer segments should be prioritized for retention or reactivation?

3. **Churn / Inactivity Risk**
   - Which customers are at risk of churn based on purchase recency?
   - What customer behaviors are associated with higher churn risk?
   - How much revenue is at risk from inactive customers?

4. **Retention**
   - How well does the business retain customers across monthly cohorts?
   - Are newer customer cohorts becoming more or less valuable?

5. **Operational Insights**
   - Which products have high return/cancellation activity?
   - Are there seasonal patterns in demand?
   - Which countries or customer groups deserve targeted marketing?

## Recommended Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, pandas, numpy |
| Database / Querying | SQLite or DuckDB, SQL |
| Visualization | Power BI, Tableau, or Plotly |
| Modeling | scikit-learn |
| Documentation | GitHub README, Jupyter Notebook |
| Optional App | Streamlit dashboard |

## Project Structure

```text
online-retail-sales-churn-analytics/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx
│   ├── interim/
│   │   └── cleaned_transactions.parquet
│   └── processed/
│       ├── monthly_sales_summary.csv
│       ├── customer_rfm_segments.csv
│       ├── customer_churn_labels.csv
│       ├── cohort_retention_matrix.csv
│       └── product_performance.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_sales_analysis.ipynb
│   ├── 04_rfm_customer_segmentation.ipynb
│   ├── 05_churn_risk_analysis.ipynb
│   └── 06_cohort_retention_analysis.ipynb
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_sales_kpis.sql
│   ├── 03_customer_rfm.sql
│   └── 04_churn_features.sql
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── rfm_segmentation.py
│   ├── churn_labeling.py
│   └── visualization.py
│
├── dashboards/
│   └── powerbi_dashboard_screenshots/
│
└── reports/
    └── executive_summary.md
```

## Analysis Plan

### 1. Data Understanding

Key checks:

- Number of rows by year
- Missing values by column
- Duplicate invoice lines
- Negative quantities
- Zero or negative prices
- Cancellation invoices
- Date range
- Number of unique customers, invoices, products, and countries

Suggested outputs:

- Data dictionary
- Data quality summary table
- Initial exploratory charts

### 2. Data Cleaning

Cleaning rules:

- Combine both yearly worksheets into one transaction table
- Standardize column names:
  - `Invoice` → `invoice_no`
  - `StockCode` → `stock_code`
  - `Description` → `description`
  - `Quantity` → `quantity`
  - `InvoiceDate` → `invoice_date`
  - `Price` → `unit_price`
  - `Customer ID` → `customer_id`
  - `Country` → `country`
- Convert invoice date to datetime
- Create `revenue = quantity * unit_price`
- Separate cancelled / returned transactions
- Remove rows with missing `customer_id` for customer-level analysis
- Keep cancellation records for return-rate analysis
- Filter out invalid prices and quantities when calculating net sales

Suggested derived columns:

| Column | Logic |
|---|---|
| revenue | `quantity * unit_price` |
| invoice_month | Month of invoice date |
| invoice_date_only | Date without timestamp |
| is_cancelled | Invoice starts with `C` or quantity < 0 |
| year_month | Monthly period |
| order_value | Sum of revenue per invoice |
| customer_first_purchase_month | First purchase month by customer |

### 3. Sales KPI Analysis

Core metrics:

- Total revenue
- Monthly revenue
- Number of orders
- Number of active customers
- Average order value
- Average basket size
- Revenue by country
- Revenue by product
- Return / cancellation rate

Visuals:

- Monthly revenue trend
- Orders and active customers by month
- Top 10 countries by revenue
- Top 10 products by revenue
- Revenue seasonality heatmap

### 4. RFM Customer Segmentation

Use a snapshot date after the last transaction date.

RFM features:

| Feature | Meaning |
|---|---|
| Recency | Days since last purchase |
| Frequency | Number of unique invoices |
| Monetary | Total customer revenue |

Segmentation logic:

- Score each customer from 1 to 5 for Recency, Frequency, and Monetary
- Combine into RFM score
- Assign business segments:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - New Customers
  - At Risk
  - Cannot Lose
  - Hibernating
  - Lost

Suggested outputs:

- Customer-level RFM table
- Segment distribution
- Revenue contribution by segment
- Recommended action by segment

### 5. Churn Risk Labeling

Since this is transaction data and not subscription data, define churn as inactivity.

Recommended churn definition:

> A customer is considered churned or inactive if they have not purchased in the last **90 days** before the analysis snapshot date.

Alternative thresholds:

- 60 days: stricter, more aggressive retention
- 90 days: balanced
- 180 days: conservative

Features for churn analysis:

| Feature | Description |
|---|---|
| recency_days | Days since last purchase |
| frequency | Number of orders |
| monetary | Total revenue |
| avg_order_value | Average revenue per order |
| customer_lifetime_days | Days between first and last purchase |
| return_rate | Share of returned/cancelled order lines |
| country | Customer country |
| unique_products | Number of unique products purchased |
| active_months | Number of months with at least one purchase |

Possible outputs:

- Churn risk table
- Churn rate by country
- Churn rate by RFM segment
- Revenue at risk
- Optional classification model: logistic regression, random forest, or XGBoost

### 6. Cohort Retention Analysis

Cohort logic:

- Define each customer’s cohort month as their first purchase month
- Track whether the customer returned in later months
- Calculate retention rate by cohort month and months since first purchase

Suggested output:

- Cohort retention matrix
- Cohort heatmap
- Interpretation of best and worst retention periods

### 7. Product and Market Analysis

Product analysis:

- Top products by revenue
- Top products by quantity
- Products with high cancellation/return count
- Products with stable repeat demand

Country analysis:

- Revenue by country
- Customers by country
- Average order value by country
- Churn risk by country

## Dashboard Design

Recommended Power BI dashboard pages:

### Page 1: Executive Overview

KPIs:

- Total revenue
- Total orders
- Active customers
- Average order value
- Return rate
- Churn / inactive customer rate

Charts:

- Monthly revenue trend
- Revenue by country
- Top products
- Customer segment distribution

### Page 2: Customer Segmentation

Charts:

- RFM segment counts
- Revenue by RFM segment
- Recency vs monetary scatter plot
- Segment action table

### Page 3: Churn Risk

Charts:

- Churn risk distribution
- Revenue at risk by segment
- Churn risk by country
- Top high-value inactive customers

### Page 4: Retention

Charts:

- Cohort retention heatmap
- Repeat purchase rate trend
- Active customers by month

## GitHub Deliverables

Minimum version:

- `README.md`
- One clean notebook: `online_retail_analysis.ipynb`
- Cleaned dataset sample or generated processed CSVs
- Dashboard screenshots
- Executive summary

Strong version:

- Modular Python scripts in `src/`
- SQL KPI queries
- Power BI dashboard screenshots
- RFM segmentation output
- Churn analysis output
- Final business recommendations

## Suggested Timeline

| Phase | Work | Estimated Output |
|---|---|---|
| Phase 1 | Data understanding and cleaning | Clean transaction table |
| Phase 2 | Sales KPI analysis | Monthly/country/product KPI tables |
| Phase 3 | RFM segmentation | Customer segment table |
| Phase 4 | Churn labeling | Customer churn risk table |
| Phase 5 | Retention analysis | Cohort retention matrix |
| Phase 6 | Dashboard | Power BI or Plotly dashboard |
| Phase 7 | Documentation | README and executive summary |

## Resume Bullets

Possible resume bullets:

- Built an end-to-end retail analytics project using Python, SQL, and Power BI on 1M+ transaction records to analyze sales trends, customer behavior, and churn risk.
- Cleaned and transformed multi-year invoice-level retail data, handling missing customer IDs, cancellation invoices, negative quantities, and invalid price records to create analysis-ready datasets.
- Developed RFM-based customer segmentation to identify high-value, loyal, at-risk, and inactive customer groups, supporting targeted retention strategies.
- Designed churn-risk labels using customer inactivity windows and engineered behavioral features including recency, frequency, monetary value, return rate, and average order value.
- Created dashboard-ready KPI tables and visualizations covering monthly revenue, average order value, customer retention, product performance, and country-level sales contribution.

## Final Business Recommendations Template

Use this section after analysis is complete:

1. **Retain high-value inactive customers**
   - Focus on customers with high monetary value but long recency.
   - Offer targeted reactivation campaigns.

2. **Prioritize champion and loyal customers**
   - Build loyalty rewards or early-access promotions.
   - Encourage repeat purchases from high-frequency customers.

3. **Investigate high-return products**
   - Review product descriptions, quality, and shipping issues.
   - Reduce return-related revenue leakage.

4. **Expand high-performing markets**
   - Identify countries with strong revenue and high average order value.
   - Prioritize localized marketing for these regions.

5. **Monitor monthly retention**
   - Use cohort retention dashboards to detect declining repeat purchase behavior early.
