from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime

from app.core.config import settings
from app.database import get_db
from app.models.utente import Utente

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")

def get_user_from_payload(payload: dict) -> Utente:
    if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
        raise HTTPException(status_code=401, detail="Token scaduto")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token non valido")

    db = next(get_db())
    user = db.query(Utente).filter(Utente.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utente non trovato")

    return user
