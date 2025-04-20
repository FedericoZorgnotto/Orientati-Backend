from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.utente import Utente
from app.services.auth import verify_user_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Security(oauth2_scheme),
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_user_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(Utente).filter(Utente.username == username).first()
    if user is None:
        raise credentials_exception

    return user
