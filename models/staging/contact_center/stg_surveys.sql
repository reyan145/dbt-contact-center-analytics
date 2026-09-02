select
    survey_id,
    call_id,
    customer_id,
    csat_score,
    nps_score,
    sentiment
from {{ source('contact_center', 'surveys') }}