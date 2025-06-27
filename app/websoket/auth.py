from datetime import datetime

from jose import jwt, JWTError

from app.core.config import settings
from app.database import get_db
from app.models.utente import Utente


class InvalidTokenError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
    except JWTError:
        raise InvalidTokenError("Token non valido o scaduto")


def get_user_from_payload(payload: dict) -> Utente:
    if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
        raise TokenExpiredError("Token scaduto")

    username = payload.get("sub")
    if not username:
        raise InvalidTokenError("Token non contiene il campo 'sub'")

    db = next(get_db())
    user = db.query(Utente).filter(Utente.username == username).first()
    if not user:
        raise UserNotFoundError(f"Utente con username '{username}' non trovato")

    return user
