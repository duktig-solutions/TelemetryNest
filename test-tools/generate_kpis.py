import json
import random
from datetime import datetime, timedelta
import pytz

# Set timezone to Asia/Yerevan
tz = pytz.timezone("Asia/Yerevan")

data = []
kpis = ['kpi1', 'kpi2', 'kpi3']
info = ['info1', 'Test Information', 'info2', 'info3']

for _ in range(2000):
    # Generate timestamp with random minutes and seconds
    now = datetime.now(tz)
    rand_min = random.randint(10, 59)
    rand_sec = random.randint(10, 59)
    timestamp = now.replace(minute=rand_min, second=rand_sec, microsecond=0)

    data.append({
        "kpi_name": random.choice(kpis),
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "tags": random.choice(info),
        "value": float(f"{random.randint(1, 500)}.{random.randint(0, 99):02}")
    })

with open("kpis.json", "w") as f:
    json.dump(data, f, indent=4)

print("Done")
