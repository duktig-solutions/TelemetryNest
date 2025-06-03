# app/services/predicted_alarm_service.py

from typing import List, Union
from ..models import predicted_alarms as predicted_alarms_model

def fetch_last_predicted_alarms(days: Union[int, None]):
    model = predicted_alarms_model.PredictedAlarms()
    return model.fetch_last_days(days)

def insert_predicted_alarms_batch(predicted_alarms: List[predicted_alarms_model.PredictedAlarm]):
    model = predicted_alarms_model.PredictedAlarms()
    model.insert_big_batch(predicted_alarms)
