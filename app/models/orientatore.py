from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base
from .gruppo import association_table_orientatori


class Orientatore(Base):
    __tablename__ = "Orientatori"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cognome: Mapped[str] = mapped_column()
    classe: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    gruppi: Mapped[List["Gruppo"]] = relationship(  # noqa: F821
        secondary=association_table_orientatori, back_populates="orientatori"
    )

    indirizzo_id: Mapped[int] = mapped_column(ForeignKey("Indirizzi.id"))
    indirizzo: Mapped["Indirizzo"] = relationship("Indirizzo", back_populates="orientatori")  # noqa: F821

    utente: Mapped[Optional["Utente"]] = relationship("Utente", back_populates="orientatore")  # noqa: F821
