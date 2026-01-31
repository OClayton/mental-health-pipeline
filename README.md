# Mental Health Data Pipeline

An automated ELT pipeline that pulls CDC mental health prevalence data and transforms it for analysis.

## Architecture
- **Extraction:** Python script using `sodapy` to fetch CDC BRFSS indicators.
- **Loading:** Data is loaded into **Google BigQuery** (Bronze layer).
- **Transformation:** **dbt** (Data Build Tool) handles the Medallion architecture.
  - `stg_mental_health`: Cleans types and renames columns (Silver).
  - `mart_mental_health_by_state`: Aggregates prevalence by geography (Gold).

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run ingestion: `python data_ingestion/ingest.py`
3. Run transformations: `cd dbt_project && dbt run`