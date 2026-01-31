# Mental Health Data Pipeline (CDC BRFSS)

**Candidate:** [Your Name]  
**Dataset:** Indicators of Anxiety or Depression Based on Reported Symptoms of Anxiety or Depression in the Last 7 Days (CDC)

## 1. Project Overview
This project implements an automated **ELT (Extract, Load, Transform)** pipeline. It extracts public health data from the CDC (Socrata API), loads it into a Google BigQuery "Bronze" layer, and utilizes **dbt (Data Build Tool)** to transform the raw data into analysis-ready Dimensional and Fact tables.



---

## 2. Architecture & Folder Structure
The project follows the **Medallion Architecture** to ensure data integrity and scalability:

* **Bronze (Raw):** Ingested API data with minimal changes.
* **Silver (Staging):** Cleaned, renamed, and cast to appropriate SQL types.
* **Gold (Mart):** Modeled into Dimensions (`dim_*`) and Facts (`fct_*`) for BI consumption.

### Directory Structure
```text
mental-health-pipeline/
├── data_ingestion/
│   └── ingest.py           # Python script for API extraction & BQ loading
├── dbt_project/
│   ├── models/
│   │   ├── staging/        # stg_mental_health.sql (Silver)
│   │   ├── marts/          # dim_locations.sql, fct_indicators.sql (Gold)
│   │   └── schema.yml      # Data tests (not_null, unique) and documentation
│   └── dbt_project.yml     # dbt project configuration
├── .gitignore              # Ensures creds.json and logs are not published
├── requirements.txt        # Python dependencies (pandas, dbt-bigquery, etc.)
└── README.md               # Project documentation