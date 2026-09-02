import pandas as pd
import random
from datetime import datetime, timedelta

# --- Parameters ---
NUM_AGENTS = 50
NUM_DAYS = 730  # 2 years (365 * 2)
START_DATE = datetime.now() - timedelta(days=NUM_DAYS)

# --- Daily Call Volume Function (Realistic Variation + Seasonality) ---
def get_calls_for_day(day_index, date_obj):
    """
    Returns a realistic number of calls for a given day.
    - Weekdays (Mon-Fri): 450-700 calls
    - Weekends (Sat-Sun): 150-400 calls
    - Summer months (Jun-Aug): +10-20% more calls
    - Winter holidays (Dec): +15-25% more calls
    - Random noise: ±80 calls
    """
    dow = day_index % 7  # 0=Monday, 6=Sunday
    month = date_obj.month
    
    # Base volume by day of week
    if dow in [0, 1, 2, 3, 4]:  # Monday-Friday
        base = random.randint(450, 650)
    else:  # Saturday-Sunday
        base = random.randint(200, 350)
    
    # Seasonality adjustments
    seasonal_factor = 1.0
    
    # Summer months (Jun, Jul, Aug) = more calls
    if month in [6, 7, 8]:
        seasonal_factor = random.uniform(1.1, 1.2)
    # December = holiday rush
    elif month == 12:
        seasonal_factor = random.uniform(1.15, 1.25)
    # January = post-holiday dip
    elif month == 1:
        seasonal_factor = random.uniform(0.85, 0.95)
    
    # Random noise
    noise = random.randint(-80, 80)
    
    # Calculate final number (ensure it's not too low)
    final = int((base * seasonal_factor) + noise)
    return max(50, final)

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
        'hire_date': (START_DATE - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
    })
df_agents = pd.DataFrame(agents)

# --- Calls ---
calls = []
call_id = 1

# Hourly volume weights (peak at 10-11 AM and 2-3 PM)
hours = list(range(8, 21))  # 8 AM to 8 PM
hour_weights = [0.03, 0.07, 0.12, 0.14, 0.08, 0.06, 0.13, 0.15, 0.10, 0.06, 0.03, 0.02, 0.01]

for day in range(NUM_DAYS):
    current_date = START_DATE + timedelta(days=day)
    calls_today = get_calls_for_day(day, current_date)
    
    for _ in range(calls_today):
        agent_id = random.randint(1, NUM_AGENTS)
        call_type = random.choices(['Inbound', 'Outbound'], weights=[0.8, 0.2])[0]
        
        # Pick hour based on peak distribution
        selected_hour = random.choices(hours, weights=hour_weights)[0]
        call_start = current_date.replace(
            hour=selected_hour, 
            minute=random.randint(0, 59), 
            second=random.randint(0, 59)
        )
        
        duration = random.randint(60, 900)  # 1-15 minutes
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

print("Data generation complete!")
print(f"Agents: {len(df_agents)}")
print(f"Calls: {len(df_calls):,}")
print(f"Surveys: {len(df_surveys):,}")