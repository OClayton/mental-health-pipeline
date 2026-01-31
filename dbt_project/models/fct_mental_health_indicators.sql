{{ config(
    materialized='table',
    partition_by={
      "field": "dbt_updated_at",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by=["state", "indicator"]
) }}

SELECT
    state,
    indicator,
    metric_percentage,
    date_range,
    dbt_updated_at
FROM {{ ref('stg_mental_health') }}