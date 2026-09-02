{{
    config(
        materialized='table'
    )
}}

select
    calls.call_id,
    calls.agent_id,
    calls.customer_id,
    calls.call_date,
    calls.call_type,
    calls.duration_seconds,
    calls.wait_time_seconds,
    calls.resolution_status,
    coalesce(surveys.csat_score, null) as csat_score,
    coalesce(surveys.nps_score, null) as nps_score,
    coalesce(surveys.sentiment, null) as sentiment
from {{ ref('stg_calls') }} calls
left join {{ ref('int_surveys_cleaned') }} surveys
    on calls.call_id = surveys.call_id