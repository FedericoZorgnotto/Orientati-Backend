from typing import Optional

from pydantic import ConfigDict, BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    username: str
    admin: bool
    temporaneo: bool
    orientatore_id: Optional[int] = None


class UserBaseAdmin(UserBase):
    id: int


class UserLogin(UserBase):
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None
    temporaneo: Optional[bool] = None
    orientatore_id: Optional[int] = None


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
