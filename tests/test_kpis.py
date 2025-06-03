# tests/test_kpis.py

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

def test_get_kpis_last():
    # Simulate a JWT token if your endpoint is protected
    # token = "Bearer your_test_token_here"

    response = client.get(
        "/kpis/last?kpi=kpi1&days=3",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_kpis():
    # token = "Bearer your_test_token_here"

    # data = [
    #     {
    #         "kpi_name": "kpi1",
    #         "timestamp": "2025-06-02 15:00:00",
    #         "value": 123.45,
    #         "tags": "test"
    #     }
    # ]
    data = generate_kpis()

    response = client.post(
        "/kpis",
        json=data,
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

def generate_kpis():
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

    return data