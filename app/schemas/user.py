from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    # username: str | None = None

class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[int] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str