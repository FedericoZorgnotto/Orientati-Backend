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

    gruppo_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Gruppi.id"))
    gruppo: Mapped[Optional["Gruppo"]] = relationship("Gruppo", back_populates="utenti")  # noqa: F821

    logs: Mapped[Optional[List["LogUtente"]]] = relationship("LogUtente", back_populates="utente")  # noqa: F821

    def __repr__(self):
        return (f"Utente(id={self.id!r}, username={self.username!r}, admin={self.admin!r},"
                f" temporaneo={self.temporaneo!r}, gruppo_id={self.gruppo_id!r})")
