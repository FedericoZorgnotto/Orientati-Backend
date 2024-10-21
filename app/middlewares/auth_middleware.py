from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.utente import Utente

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def admin_access(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(Utente).filter(Utente.username == username).first()
        if not user or not user.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise credentials_exception
