with surveys as (
    select
        s.*,
        c.resolution_status,
        c.call_type,
        c.wait_time_seconds
    from {{ ref('stg_surveys') }} s
    left join {{ ref('stg_calls') }} c using (call_id)
)

select
    survey_id,
    call_id,
    customer_id,
    case
        when resolution_status = 'Unresolved' and csat_score = 5 then 1
        else csat_score
    end as csat_score,
    nps_score,
    sentiment,
    resolution_status,   -- include this so tests can filter
    call_type,
    wait_time_seconds
from surveys