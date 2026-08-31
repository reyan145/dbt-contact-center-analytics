select
    agent_id,
    name,
    team,
    shift,
    hire_date
from {{ source('contact_center', 'agents') }}