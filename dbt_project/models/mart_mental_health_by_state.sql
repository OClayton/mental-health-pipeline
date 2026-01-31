{{ config(materialized='table') }}

SELECT
    state,
    indicator,
    AVG(metric_percentage) AS avg_prevalence,
    COUNT(*) AS data_points_count
FROM {{ ref('stg_mental_health') }}
GROUP BY 1, 2