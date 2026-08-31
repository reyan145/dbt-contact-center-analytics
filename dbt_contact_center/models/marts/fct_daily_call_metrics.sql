with daily as (
    select * from {{ ref('int_daily_call_metrics') }}
)

select
    call_date,
    total_calls,
    round(avg_handle_time, 2) as avg_handle_time,
    round(avg_wait_time, 2) as avg_wait_time,
    round(safe_divide(resolved_calls, total_calls) * 100, 2) as fcr_rate,
    round(safe_divide(answered_within_30s, total_calls) * 100, 2) as service_level,
    round(avg_csat, 2) as avg_csat,
    inbound_calls,
    outbound_calls
from daily