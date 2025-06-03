# app/services/auth_service.py

from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
import bcrypt
from ..models import user as user_model
from ..settings import Settings

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def get_user(email: str):
    model = user_model.User()
    return model.fetch_user_by_where({"email": email})

def authenticate_user(req_usr):
    db_user = get_user(req_usr.email)
    if not db_user:
        return False
    if not verify_password(req_usr.password, db_user['password'].encode()):
        return False
    return req_usr

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Settings.JWT_SECRET, algorithm=Settings.JWT_ALGORITHM)
