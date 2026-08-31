-- CSAT should not be 5 (Excellent) if the call was Unresolved
select
    call_id,
    csat_score,
    resolution_status
from {{ ref('int_surveys_cleaned') }}
where resolution_status = 'Unresolved' and csat_score = 5