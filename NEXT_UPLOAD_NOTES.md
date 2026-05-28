# Next Upload Notes

After uploading these files, your repository will have a stronger project structure:

- Two runnable notebooks for cleaning, EDA, RFM segmentation, churn risk, and cohort retention
- A reusable pipeline script in `src/run_pipeline.py`
- Additional feature engineering and visualization modules
- SQL churn feature query
- Dashboard build guide for Power BI or Tableau

## How to Run Locally

1. Put the raw dataset here:

```text
data/raw/online_retail_II.xlsx
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the pipeline:

```bash
python src/run_pipeline.py
```

4. The output CSVs will be saved here:

```text
data/processed/
```
