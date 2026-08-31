with calls as (
    select * from {{ ref('stg_calls') }}
),
surveys as (
    select * from {{ ref('int_surveys_cleaned') }}
)

select
    calls.call_date,
    count(calls.call_id) as total_calls,
    avg(calls.duration_seconds) as avg_handle_time,
    avg(calls.wait_time_seconds) as avg_wait_time,          -- qualified with calls
    sum(case when calls.resolution_status = 'Resolved' then 1 else 0 end) as resolved_calls,
    sum(case when calls.wait_time_seconds <= 30 then 1 else 0 end) as answered_within_30s,
    sum(case when calls.call_type = 'Inbound' then 1 else 0 end) as inbound_calls,
    sum(case when calls.call_type = 'Outbound' then 1 else 0 end) as outbound_calls,
    avg(surveys.csat_score) as avg_csat                     -- qualified with surveys
from calls
left join surveys on calls.call_id = surveys.call_id
group by 1