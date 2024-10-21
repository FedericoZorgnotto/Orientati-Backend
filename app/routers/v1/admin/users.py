from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.utente import Utente
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserList
from app.services.auth import get_password_hash

users_router = APIRouter()


@users_router.get("/users", response_model=UserList)
async def get_all_users(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli utenti dal database
    """

    UserList.users = db.query(Utente).all()
    return UserList


@users_router.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un utente dal database
    """
    if not db.query(Utente).filter(Utente.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user = db.query(Utente).filter(Utente.id == user_id).first()
        return user
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@users_router.post("/users", response_model=UserBase)
async def create_user(user: UserCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un utente nel database
    """
    hashed_password = get_password_hash(user.password)

    db_user = Utente(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
        name=user.name,
        surname=user.surname
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), _=Depends(admin_access)):  # noqa: C901, E501
    """
    Aggiorna un utente nel database
    """
    db_user = db.query(Utente).filter(Utente.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Aggiorna i campi se sono stati forniti
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.hashed_password = get_password_hash(user_update.password)  # Hascia la nuova password
    if user_update.is_admin is not None:
        db_user.admin = user_update.is_admin
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.surname is not None:
        db_user.surname = user_update.surname

    db.commit()
    db.refresh(db_user)

    return {"msg": "User updated successfully."}


@users_router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un utente dal database
    """
    if not db.query(Utente).filter(Utente.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.query(Utente).filter(Utente.id == user_id).delete()
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="User has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
