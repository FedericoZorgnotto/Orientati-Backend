from __future__ import annotations

import datetime
import enum
from typing import Optional

import pytz
from sqlalchemy import DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CategoriaLogUtente(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogUtente(Base):
    __tablename__ = 'user_action_logs'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    utente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Utenti.id"), index=True, nullable=True, default=None)
    categoria: Mapped[CategoriaLogUtente] = mapped_column(
        Enum(CategoriaLogUtente), nullable=False, default=CategoriaLogUtente.INFO
    )
    azione: Mapped[str] = mapped_column(nullable=False)
    dati: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    orario: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(pytz.timezone("Europe/Rome")), nullable=False
    )
    utente: Mapped[Optional["Utente"]] = relationship("Utente", back_populates="logs")  # noqa: F821

    def __repr__(self):
        return (f"LogUtente(id={self.id!r}, utente_id={self.utente_id!r}, categoria={self.categoria!r},"
                f" azione={self.azione!r}, dati={self.dati!r}, orario={self.orario!r})")
