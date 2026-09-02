{{
    config(
        materialized='table'
    )
}}

with calls as (
    select
        agent_id,
        call_date,
        call_id,
        duration_seconds,
        wait_time_seconds,
        resolution_status,
        csat_score
    from {{ ref('fct_call_metrics') }}
)

select
    agent_id,
    call_date,
    count(call_id) as total_calls,
    avg(duration_seconds) as avg_handle_time,
    avg(wait_time_seconds) as avg_wait_time,
    sum(case when resolution_status = 'Resolved' then 1 else 0 end) as resolved_calls,
    round(safe_divide(sum(case when resolution_status = 'Resolved' then 1 else 0 end), count(call_id)) * 100, 2) as fcr_rate,
    sum(case when wait_time_seconds <= 30 then 1 else 0 end) as answered_within_30s,
    round(safe_divide(
        sum(case when wait_time_seconds <= 30 then 1 else 0 end),
        count(call_id)
    ) * 100, 2) as service_level_pct,
    avg(csat_score) as avg_csat
from calls
group by 1, 2