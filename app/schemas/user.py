from typing import Optional

from pydantic import ConfigDict, BaseModel, EmailStr

"""
 id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    name: Mapped[Optional[str]]
    surname: Mapped[Optional[str]]
    year: Mapped[Optional[int]]
    section: Mapped[Optional[str]]

    specialisation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("specialisations.id"))
    specialisation: Mapped[Optional["Specialisation"]] = relationship(back_populates="users")

    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Optional["Group"]] = relationship(back_populates="users")
"""


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
    year: Optional[int] = None
    section: Optional[str] = None
    specialisation_id: Optional[int] = None
    group_id: Optional[int] = None


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
