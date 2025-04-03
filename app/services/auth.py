from datetime import datetime, timedelta

import pytz
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.timezone("Europe/Rome")) + expires_delta
    else:
        expire = (datetime.now(pytz.timezone("Europe/Rome"))
                  + timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire, "user_id": data.get("user_id")})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.timezone("Europe/Rome")) + expires_delta
    else:
        expire = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "user_id": data.get("user_id")})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        return payload  # Restituisce i dati decodificati dal token
    except JWTError:
        return None
