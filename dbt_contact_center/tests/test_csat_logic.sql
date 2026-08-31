-- CSAT should not be 5 (Excellent) if the call was Unresolved
select
    call_id,
    csat_score,
    resolution_status
from {{ ref('stg_surveys') }}
left join {{ ref('stg_calls') }} using (call_id)
where resolution_status = 'Unresolved' and csat_score >= 4