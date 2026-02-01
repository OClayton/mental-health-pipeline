# Mental Health Data Pipeline

An end-to-end data engineering pipeline that ingests CDC mental health indicators, transforms the data using dbt, and visualizes trends in Looker Studio.

## Project Overview
This project tracks symptoms of anxiety and depression across the United States. It automates the flow of data from the CDC Socrata API into Google BigQuery, using dbt for sophisticated data modeling and cleaning.



---

## Architecture
* **Ingestion:** Python script using the sodapy library to pull from the CDC's "Indicators of Anxiety or Depression" API.
* **Storage:** Google BigQuery (Data Warehouse).
* **Transformation:** dbt (Data Build Tool) utilizing a Bronze/Silver/Gold modeling structure.
* **BI:** Looker Studio for geospatial and time-series analysis.

---

## Technical Challenges and Solutions
* **Dynamic Date Parsing:** The raw CDC data provided timestamps as ISO 8601 strings (e.g., 2020-09-16T00:00:00.000). I implemented SAFE_CAST and DATE() functions in dbt to transform these into clean, sortable date objects, preventing null errors in the dashboard.
* **Schema Synchronization:** Resolved a persistent Looker Studio Error ID: 6d5d1be5 by performing a deep refresh of the metadata schema and re-mapping geographic dimensions.
* **National Benchmarking:** Filtered out national-level "United States" totals from the primary dataset to ensure the Geo Map correctly rendered individual state data, while retaining the national data for baseline KPIs.

---

## Time Spent

**Total Estimated Work Time:** ~4.5 Hours

| Phase | Time | Key Tasks |
| :--- | :--- | :--- |
| **Data Ingestion** | 45m | Python script setup, CDC Socrata API integration, and BigQuery landing. |
| **dbt Development** | 2h 15m | Model creation, debugging Regex/Date logic, and fixing table-name mismatches. |
| **BI and Visualization** | 1h 15m | Looker Studio setup, Geo-mapping, and resolving schema alignment errors. |
| **Documentation** | 15m | README finalization and project structure organization. |

---

## Project Structure
* `/ingest.py`: Python script for API data extraction.
* `/dbt_project/models/staging`: Silver layer (cleaning and casting).
* `/dbt_project/models/marts`: Gold layer (final analytics-ready tables).
* `/creds.json`: (Not included in repo) GCP Service Account credentials.

---

## How to Run
1. **Ingest:** Run `python ingest.py` to populate BigQuery.
2. **Transform:** Navigate to the dbt directory and run `dbt run --full-refresh`.
3. **Visualize:** Connect the `fct_mental_health_indicators` table to Looker Studio.