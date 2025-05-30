from __future__ import annotations

import random
import string
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Gruppo(Base):
    __tablename__ = "Gruppi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    codice: Mapped[Optional[str]] = mapped_column()
    fasciaOraria_id: Mapped[int] = mapped_column(ForeignKey("FasceOrarie.id"))
    numero_tappa: Mapped[Optional[int]] = mapped_column()
    arrivato: Mapped[Optional[bool]] = mapped_column()
    orario_partenza_effettivo: Mapped[Optional[str]] = mapped_column()
    orario_fine_effettivo: Mapped[Optional[str]] = mapped_column()

    fasciaOraria: Mapped["FasciaOraria"] = relationship("FasciaOraria", back_populates="gruppi")  # noqa: F821
    iscrizioni: Mapped[List["Iscrizione"]] = relationship("Iscrizione", back_populates="gruppo")  # noqa: F821
    utenti: Mapped[List["Utente"]] = relationship("Utente", back_populates="gruppo")  # noqa: F821
    presenti: Mapped[List["Presente"]] = relationship("Presente", back_populates="gruppo")  # noqa: F821
    assenti: Mapped[List["Assente"]] = relationship("Assente", back_populates="gruppo")  # noqa: F821

    @classmethod
    def genera_codice(cls):
        return ''.join(random.choices(string.ascii_uppercase, k=3))
        pass

    def __repr__(self):
        return f"Gruppo(id={self.id!r}, nome={self.nome!r}, codice={self.codice!r}, fasciaOraria_id={self.fasciaOraria_id!r})"