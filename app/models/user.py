from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

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
