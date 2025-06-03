# app/routers/predicted_alarms_router.py

from fastapi import APIRouter, Depends, Body
from typing_extensions import Annotated
from ..models import predicted_alarms as predicted_alarms_model
from ..services import predicted_alarms_service
from ..dependencies import decode_jwt
from typing import List, Union

tokenPayload = Annotated[dict, Depends(decode_jwt)]
router = APIRouter()

@router.get("/predicted-alarms/last", tags=["predicted_alarms"])
async def get_predicted_alarms_last(payload: tokenPayload, days: Union[int, None] = 7):
    return predicted_alarms_service.fetch_last_predicted_alarms(days)

@router.post("/predicted-alarms", tags=["predicted_alarms"])
async def create_predicted_alarms(payload: tokenPayload, predicted_alarms: List[predicted_alarms_model.PredictedAlarm]):
    predicted_alarms_service.insert_predicted_alarms_batch(predicted_alarms)
    return {"message": "ok"}
