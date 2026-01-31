{{ config(materialized='table') }}

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['state']) }} as location_key,
    state as state_name
FROM {{ ref('stg_mental_health') }}