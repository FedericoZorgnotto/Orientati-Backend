from typing import Optional

from pydantic import ConfigDict, BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    # username: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool
    name: Optional[str] = None
    surname: Optional[str] = None
    year: Optional[int] = None
    section: Optional[str] = None
    specialisation_id: Optional[int] = None
    group_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[User]
    model_config = ConfigDict(from_attributes=True)
