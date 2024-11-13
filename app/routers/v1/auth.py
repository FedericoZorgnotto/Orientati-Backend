import random
import string

import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Utente
from app.schemas.utente import Token, PasswordChange, UserBase, RefreshTokenRequest
from app.services.auth import verify_password, get_password_hash, create_access_token, create_refresh_token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Questo metodo permette di effettuare il login
    """
    user = db.query(Utente).filter(Utente.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})  # Genera il refresh token

    # response.headers["Access-Control-Allow-Origin"] = "*"
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/token/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token,
            "token_type": "bearer",
            "refresh_token": request.refresh_token}


@router.get("/utenti/me", response_model=UserBase)
async def read_users_me(utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Questo metodo permette di ottenere i dati dell'utente attualmente autenticato
    """
    connesso_a_gruppo = False

    message = {
        "username": utente.username,
        "admin": utente.admin,
        "temporaneo": utente.temporaneo,
        "connessoAGruppo": connesso_a_gruppo
    }
    return message


# request a temp user
@router.post("/utenti/temp", response_model=Token)
async def create_temp_user(db: Session = Depends(get_db)):
    """
    This method allows to create a temporary user
    """
    randomUsername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    db_user = Utente(
        username=randomUsername,
        hashed_password="noAuth",
        admin=False,
        temporaneo=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/utenti/me/change_password")
async def change_password(password_change: PasswordChange, db: Session = Depends(get_db),
                          current_user: Utente = Depends(get_current_user)):
    """
    This method allows the currently authenticated user to change their password
    """
    db_user = db.query(Utente).filter(Utente.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.temporaneo:
        raise HTTPException(status_code=400, detail="Temp users cannot change their password")

    if not verify_password(password_change.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    db_user.hashed_password = get_password_hash(password_change.new_password)

    db.commit()
    db.refresh(db_user)

    return {"msg": "Password updated successfully."}
