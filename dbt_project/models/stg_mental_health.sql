{{ config(materialized='view') }}

SELECT
    state,
    indicator,
    -- In this dataset, the column is 'group' (which is a reserved word, so use backticks)
    `group` AS demographic_group,
    -- The raw 'value' is a string; we need it as a float
    SAFE_CAST(value AS FLOAT64) AS metric_percentage,
    -- Use time_period and time_period_label
    time_period_label AS date_range,
    CURRENT_TIMESTAMP() AS dbt_updated_at
FROM {{ source('cdc_raw', 'raw_cdc_brfss') }}
WHERE value IS NOT NULL