# Project Planning Notes

## Best Project Title Options

1. Online Retail Sales & Customer Churn Analytics
2. Customer Segmentation and Churn Risk Analysis for Online Retail
3. End-to-End Retail Analytics: Sales, RFM Segmentation, and Retention
4. Retail BI Dashboard and Customer Churn Analysis

Recommended title for resume:

**Online Retail Sales & Customer Churn Analytics**

## Why This Project Fits Your Resume

This project is strong for data analyst / BI analyst roles because it shows:

- Real transaction-level data cleaning
- Business KPI design
- SQL-style aggregation
- Customer analytics
- Churn and retention thinking
- Dashboard readiness
- Python + SQL + Power BI workflow

It can connect well with your existing retail churn project and BI dashboard experience.

## Skill Mapping

| Resume Skill | How This Project Shows It |
|---|---|
| Python | Cleaning, feature engineering, RFM scoring, churn labeling |
| SQL | KPI queries, customer aggregation, cohort logic |
| Power BI | Dashboard and executive reporting |
| Data Cleaning | Missing values, cancellations, returns, invalid transactions |
| Customer Analytics | RFM, churn risk, retention cohorts |
| Business Analysis | Recommendations for retention, product, and market strategy |
| Statistics | Segmentation, distributions, churn-rate comparison |
| Machine Learning | Optional churn classifier |

## Suggested Notebook Flow

### Notebook 1: Data Understanding

Sections:

1. Load two sheets
2. Check shape and columns
3. Missing value analysis
4. Cancellation and return analysis
5. Date range and customer coverage
6. Initial observations

### Notebook 2: Data Cleaning

Sections:

1. Standardize column names
2. Combine yearly sheets
3. Create revenue column
4. Flag cancelled transactions
5. Remove invalid records for sales analysis
6. Save cleaned dataset

### Notebook 3: Sales Analysis

Sections:

1. Monthly revenue trend
2. Monthly order volume
3. Average order value
4. Country performance
5. Product performance
6. Return and cancellation analysis

### Notebook 4: RFM Segmentation

Sections:

1. Create customer-level table
2. Calculate recency, frequency, monetary
3. Score RFM dimensions
4. Assign customer segments
5. Segment-level business interpretation

### Notebook 5: Churn Risk

Sections:

1. Define churn threshold
2. Create churn label
3. Build customer behavior features
4. Analyze churn rate by segment and country
5. Calculate revenue at risk
6. Optional model

### Notebook 6: Cohort Retention

Sections:

1. Identify first purchase month
2. Build cohort index
3. Calculate active customers by cohort
4. Calculate retention rate
5. Visualize cohort heatmap

## Minimum Viable GitHub Version

If you want to finish quickly, build this version first:

1. One notebook: `online_retail_sales_churn_analysis.ipynb`
2. README with project explanation
3. Three output CSVs:
   - `monthly_sales_summary.csv`
   - `customer_rfm_segments.csv`
   - `customer_churn_labels.csv`
4. 4–6 dashboard screenshots
5. Resume bullet section

## Strong GitHub Version

To make it look more professional:

1. Split the work into multiple notebooks
2. Add reusable scripts in `src/`
3. Add SQL queries
4. Add dashboard screenshots
5. Add executive summary
6. Add clear business recommendations

## Recommended Final GitHub README Sections

1. Project Overview
2. Business Problem
3. Dataset Description
4. Data Cleaning Process
5. Key Metrics
6. RFM Segmentation
7. Churn Risk Definition
8. Dashboard Preview
9. Key Insights
10. Business Recommendations
11. Tools Used
12. How to Run
13. Resume Highlights
