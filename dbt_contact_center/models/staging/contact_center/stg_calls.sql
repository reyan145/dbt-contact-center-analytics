select
    call_id,
    agent_id,
    customer_id,
    call_type,
    call_start,
    call_end,
    duration_seconds,
    wait_time_seconds,
    resolution_status,
    cast(call_start as date) as call_date,
    extract(hour from call_start) as call_hour
from {{ source('contact_center', 'calls') }}