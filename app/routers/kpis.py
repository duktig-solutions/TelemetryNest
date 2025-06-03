# app/routers/kpi_router.py

from fastapi import APIRouter, Depends, Body
from typing_extensions import Annotated
from ..models import kpis as kpi_model
from ..dependencies import decode_jwt
from ..services import kpi_service
from typing import List, Union

tokenPayload = Annotated[dict, Depends(decode_jwt)]
router = APIRouter()

@router.get("/kpis/last", tags=["kpi"])
async def get_kpis_last(payload: tokenPayload, kpi: Union[str, None] = 'kpi1', days: Union[int, None] = 7):
    return kpi_service.fetch_last_kpis(kpi, days)

@router.post("/kpis", tags=["kpi"])
async def create_kpis(payload: tokenPayload, kpis: List[kpi_model.Kpi]):
    kpi_service.insert_kpis_batch(kpis)
    return {"message": "ok"}
