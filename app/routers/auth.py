
from fastapi import APIRouter, Body, Response, status
from ..models import user
from ..services import auth_service
from datetime import timedelta
from ..settings import Settings

router = APIRouter()

@router.post("/user/login", tags=["user"])
def user_login(response: Response, user_param: user.UserLoginSchema = Body(...)):
    if auth_service.authenticate_user(user_param):
        token_expiry = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return auth_service.create_access_token(
            data={"email": user_param.email}, expires_delta=token_expiry
        )
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"error": "Wrong login details!"}
