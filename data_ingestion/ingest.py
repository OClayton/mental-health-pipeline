import os
import pandas as pd
from google.cloud import bigquery
from sodapy import Socrata

# 1. AUTHENTICATION
# Points to the creds.json in your root folder
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../creds.json"

# 2. CONFIGURATION
PROJECT_ID = "avid-atlas-433914-r2"
DATASET_ID = "orie_clayton_mental_health"
TABLE_NAME = "raw_cdc_brfss"

# Construct the full ID: project.dataset.table
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

# Socrata API Config: Indicators of Anxiety or Depression
# Dataset Link: https://data.cdc.gov/NCHS/Indicators-of-Anxiety-or-Depression-Based-on-Repor/yni7-er2q
CDC_DOMAIN = "data.cdc.gov"
CDC_DATASET_IDENTIFIER = "yni7-er2q" 

def run_ingestion():
    print("🚀 Starting ingestion from CDC Socrata API...")
    
    # Initialize Clients
    # We use None for the app_token because we are under the 1,000 row/hour unauthenticated limit
    socrata_client = Socrata(CDC_DOMAIN, None)
    bq_client = bigquery.Client(project=PROJECT_ID)

    try:
        # 3. PULL DATA
        print(f"📡 Requesting dataset {CDC_DATASET_IDENTIFIER}...")
        results = socrata_client.get(CDC_DATASET_IDENTIFIER, limit=5000)
        df = pd.DataFrame.from_records(results)
        
        # 4. MINIMAL VALIDATION
        print("🔍 Validating data...")
        
        # Row count check
        row_count = len(df)
        if row_count == 0:
            raise ValueError("Validation Failed: No rows retrieved from API.")
        
        # Schema/Column expectation check for yni7-er2q dataset
        # Common columns: 'state', 'indicator', 'value', 'time_period'
        required_columns = ['state', 'indicator', 'value']
        for col in required_columns:
            if col not in df.columns:
                available = df.columns.tolist()
                raise KeyError(f"Validation Failed: Missing column '{col}'. Available: {available}")
        
        # Basic Null check on 'state'
        null_count = df['state'].isnull().sum()
        if null_count > (row_count * 0.1):
            print(f"⚠️ Warning: High null count detected in 'state' ({null_count} rows).")

        # 5. LOAD TO BIGQUERY
        print(f"📤 Loading {row_count} rows to BigQuery: {FULL_TABLE_ID}...")
        
        # job_config ensures we overwrite the table each time (WRITE_TRUNCATE)
        # autodetect=True allows BQ to infer schema from the DataFrame
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,
        )

        job = bq_client.load_table_from_dataframe(df, FULL_TABLE_ID, job_config=job_config)
        job.result() # Wait for the load job to complete
        
        print(f"✅ Success! Data loaded to {FULL_TABLE_ID}")

    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
    finally:
        socrata_client.close()

if __name__ == "__main__":
    run_ingestion()