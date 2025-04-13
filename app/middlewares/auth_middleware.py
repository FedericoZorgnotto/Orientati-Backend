from datetime import datetime

from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.models import Genitore
from app.models.utente import Utente

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def admin_access(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code=401, detail="Token has expired")
        user = db.query(Utente).filter(Utente.username == username).first()
        if not user or not user.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise credentials_exception


async def genitore_access(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code=401, detail="Token has expired")
        genitore = db.query(Genitore).filter(Genitore.email == email).first()
        if not genitore:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise credentials_exception
    return genitore


async def genitoreRegistrato_access(request: Request, db: Session = Depends(get_db),
                                    token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code=401, detail="Token has expired")
        genitore = db.query(Genitore).filter(Genitore.email == email).first()
        if not genitore or not genitore.comune or not genitore.nome or not genitore.cognome:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise credentials_exception
    pass
