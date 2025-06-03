# app/routers/profile_router.py

from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from ..dependencies import decode_jwt
from ..services import profile_service

tokenPayload = Annotated[dict, Depends(decode_jwt)]
router = APIRouter()

@router.get("/profile", tags=["profile"])
async def read_get_profile_info(payload: tokenPayload):
    return profile_service.get_profile_info(payload['email'])
