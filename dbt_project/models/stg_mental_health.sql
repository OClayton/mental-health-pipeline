with source as (
    select * from {{ source('mental_health', 'raw_cdc_brfss') }}
)

select
    -- Cast the native CDC timestamps into simple Date objects
	date(safe_cast(time_period_start_date as timestamp)) as start_date,
    date(safe_cast(time_period_end_date as timestamp)) as end_date,

    -- Keep the label for context if needed
    time_period_label,

    state,
    indicator,
    cast(value as float64) as metric_percentage
from source