import json
import random
from datetime import datetime
import pytz

# Set timezone to Asia/Yerevan
tz = pytz.timezone("Asia/Yerevan")

data = []
alert_signs = ['YES', 'NO']
severities = ['CRITICAL', 'MAJOR', 'MINOR', 'INFORMATION']

for i in range(1, 2001):
    now = datetime.now(tz)
    rand_min = random.randint(10, 59)
    rand_sec = random.randint(10, 59)
    timestamp = now.replace(minute=rand_min, second=rand_sec, microsecond=0)

    data.append({
        "operator_id": 456,
        "date_prediction": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "alert_sign": random.choice(alert_signs),
        "element_id": random.randint(100, 1000),
        "fault_description": f"Fault description {i}",
        "fault_id": random.randint(100, 3432),
        "fault_name": f"Fault name {i}",
        "object": f"object@name{i}",
        "probability": float(f"{random.randint(100, 1000)}.{random.randint(10, 99):02}"),
        "severity": random.choice(severities)
    })

# Write to alarms-data.json with pretty formatting
with open("alarms-data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Done")
