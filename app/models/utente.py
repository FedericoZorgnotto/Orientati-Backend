from __future__ import annotations

from typing import Optional, List

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Utente(Base):
    __tablename__ = "Utenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    temporaneo: Mapped[bool] = mapped_column(Boolean, default=False)

    orientatore_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Orientatori.id"))
    orientatore: Mapped[Optional["Orientatore"]] = relationship("Orientatore", back_populates="utente")  # noqa: F821

    logs: Mapped[Optional[List["LogUtente"]]] = relationship("LogUtente", back_populates="utente") # noqa: F821

    def __repr__(self):
        return (f"Utente(id={self.id!r}, username={self.username!r}, admin={self.admin!r},"
                f" temporaneo={self.temporaneo!r}, orientatore_id={self.orientatore_id!r})")
