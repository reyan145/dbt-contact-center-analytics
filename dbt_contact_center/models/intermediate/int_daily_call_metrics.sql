with calls as (
    select * from {{ ref('stg_calls') }}
),
surveys as (
    select * from {{ ref('stg_surveys') }}
)

select
    call_date,
    count(call_id) as total_calls,
    avg(duration_seconds) as avg_handle_time,
    avg(wait_time_seconds) as avg_wait_time,
    sum(case when resolution_status = 'Resolved' then 1 else 0 end) as resolved_calls,
    sum(case when wait_time_seconds <= 30 then 1 else 0 end) as answered_within_30s,
    sum(case when call_type = 'Inbound' then 1 else 0 end) as inbound_calls,
    sum(case when call_type = 'Outbound' then 1 else 0 end) as outbound_calls,
    avg(csat_score) as avg_csat
from calls
left join surveys using (call_id)
group by 1