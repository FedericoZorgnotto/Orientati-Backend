from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models.user import User
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserList
from app.services.auth import get_password_hash

users_router = APIRouter()


@users_router.get("/users", response_model=UserList)
async def get_all_users(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti gli utenti dal database
    """

    UserList.users = db.query(User).all()
    return UserList


@users_router.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un utente dal database
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user


@users_router.post("/users", response_model=UserBase)
async def create_user(user: UserCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un utente nel database
    """
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
        name=user.name,
        surname=user.surname,
        year=user.year,
        section=user.section,
        specialisation_id=user.specialisation_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Aggiorna un utente nel database
    """
    db_user = db.query(User).filter(User.id == user_id).first()

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
        db_user.is_admin = user_update.is_admin
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.surname is not None:
        db_user.surname = user_update.surname
    if user_update.year is not None:
        db_user.year = user_update.year
    if user_update.section is not None:
        db_user.section = user_update.section
    if user_update.specialisation_id is not None:
        db_user.specialisation_id = user_update.specialisation_id

    db.commit()
    db.refresh(db_user)

    return {"msg": "User updated successfully."}


@users_router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un utente dal database
    """
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted successfully"}
