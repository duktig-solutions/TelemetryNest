# tests/test_alarms.py

from fastapi.testclient import TestClient
from app.main import app
from conftest import TEST_EMAIL, TEST_PASSWORD
import random
from datetime import datetime, timedelta
import pytz

client = TestClient(app)

token = ""

def test_auth():

    data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    response = client.post(
        "/user/login",
        json=data
    )

    assert response.status_code == 200

    global token
    token = "Bearer " + response.json()

def test_get_alarms_last():
    # Simulate a JWT token if your endpoint is protected
    # token = "Bearer your_test_token_here"

    response = client.get(
        "/predicted-alarms/last",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_alarms():

    data = generate_alarms()

    response = client.post(
        "/predicted-alarms",
        json=data,
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

def generate_alarms():
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

    return data