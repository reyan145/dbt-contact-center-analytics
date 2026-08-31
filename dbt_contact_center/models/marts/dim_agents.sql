select
    agent_id,
    name,
    team,
    shift
from {{ ref('stg_agents') }}