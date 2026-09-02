{{
    config(
        materialized='table'
    )
}}

with daily as (
    select * from {{ ref('int_daily_call_metrics') }}
)

select
    call_date,
    total_calls,
    round(avg_handle_time, 2) as avg_handle_time,
    round(avg_wait_time, 2) as avg_wait_time,
    {{ calculate_rate('resolved_calls', 'total_calls') }} as fcr_rate,
    {{ calculate_rate('answered_within_30s', 'total_calls') }} as service_level,
    round(avg_csat, 2) as avg_csat,
    inbound_calls,
    outbound_calls
from daily

{% if is_incremental() %}
    where call_date > (select max(call_date) from {{ this }})
{% endif %}