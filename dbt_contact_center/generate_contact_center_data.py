import pandas as pd
import random
from datetime import datetime, timedelta

# --- Parameters ---
NUM_AGENTS = 50
NUM_DAYS = 30
CALLS_PER_DAY = 500
START_DATE = datetime.now() - timedelta(days=NUM_DAYS)

# --- Agents ---
teams = ['Sales', 'Support', 'Tech', 'Billing']
shifts = ['Morning', 'Evening', 'Night']
agents = []
for i in range(1, NUM_AGENTS + 1):
    agents.append({
        'agent_id': i,
        'name': f'Agent_{i}',
        'team': random.choice(teams),
        'shift': random.choice(shifts),
        'hire_date': (START_DATE - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
    })
df_agents = pd.DataFrame(agents)

# --- Calls ---
calls = []
call_id = 1

# Hourly volume weights (peak at 10-11 AM and 2-3 PM)
hours = list(range(8, 21))
hour_weights = [0.03, 0.07, 0.12, 0.14, 0.08, 0.06, 0.13, 0.15, 0.10, 0.06, 0.03, 0.02, 0.01]

for day in range(NUM_DAYS):
    current_date = START_DATE + timedelta(days=day)
    for _ in range(CALLS_PER_DAY):
        agent_id = random.randint(1, NUM_AGENTS)
        call_type = random.choices(['Inbound', 'Outbound'], weights=[0.8, 0.2])[0]
        
        # Pick hour based on peak distribution
        selected_hour = random.choices(hours, weights=hour_weights)[0]
        call_start = current_date.replace(
            hour=selected_hour, 
            minute=random.randint(0, 59), 
            second=random.randint(0, 59)
        )
        
        duration = random.randint(60, 900)
        call_end = call_start + timedelta(seconds=duration)
        
        # Outbound calls don't have wait time
        wait_time = random.randint(0, 180) if call_type == 'Inbound' else 0
        
        resolution = random.choices(['Resolved', 'Escalated', 'Unresolved'], weights=[0.75, 0.15, 0.10])[0]

        calls.append({
            'call_id': call_id,
            'agent_id': agent_id,
            'customer_id': random.randint(1000, 9999),
            'call_type': call_type,
            'call_start': call_start,
            'call_end': call_end,
            'duration_seconds': duration,
            'wait_time_seconds': wait_time,
            'resolution_status': resolution
        })
        call_id += 1

df_calls = pd.DataFrame(calls)

# --- Surveys (Correlated to Call Outcome) ---
surveys = []
survey_id = 1

# 30% survey response rate
survey_calls = df_calls.sample(frac=0.3).to_dict('records')

for call in survey_calls:
    # CSAT logic: wait time + resolution → satisfaction
    if call['resolution_status'] == 'Resolved' and call['wait_time_seconds'] < 45:
        csat = random.choices([5, 4, 3, 2, 1], weights=[0.6, 0.25, 0.1, 0.03, 0.02])[0]
        sentiment = random.choices(['Positive', 'Neutral', 'Negative'], weights=[0.7, 0.2, 0.1])[0]
    elif call['resolution_status'] == 'Unresolved' or call['wait_time_seconds'] > 120:
        csat = random.choices([5, 4, 3, 2, 1], weights=[0.0, 0.05, 0.15, 0.35, 0.45])[0]
        sentiment = random.choices(['Positive', 'Neutral', 'Negative'], weights=[0.1, 0.2, 0.7])[0]
    else:
        csat = random.choices([5, 4, 3, 2, 1], weights=[0.2, 0.4, 0.25, 0.1, 0.05])[0]
        sentiment = random.choices(['Positive', 'Neutral', 'Negative'], weights=[0.3, 0.5, 0.2])[0]

    nps_base = csat * 2
    nps_score = max(0, min(10, nps_base + random.randint(-1, 1)))

    surveys.append({
        'survey_id': survey_id,
        'call_id': call['call_id'],
        'customer_id': call['customer_id'],
        'csat_score': csat,
        'nps_score': nps_score,
        'sentiment': sentiment
    })
    survey_id += 1

df_surveys = pd.DataFrame(surveys)

# --- Export ---
df_agents.to_csv('seeds/agents.csv', index=False)
df_calls.to_csv('seeds/calls.csv', index=False)
df_surveys.to_csv('seeds/surveys.csv', index=False)