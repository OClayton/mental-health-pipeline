with staging as (
    select * from {{ ref('stg_mental_health') }}
)

select
    start_date,
    end_date,
    state,
    indicator,
    metric_percentage
from staging