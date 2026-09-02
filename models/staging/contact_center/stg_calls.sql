select
    call_id,
    agent_id,
    customer_id,
    call_type,
    cast(call_start as timestamp) as call_start,
    cast(call_end as timestamp) as call_end,
    duration_seconds,
    wait_time_seconds,
    resolution_status,
    date(cast(call_start as timestamp)) as call_date,
    extract(hour from cast(call_start as timestamp)) as call_hour
from {{ source('contact_center', 'calls') }}