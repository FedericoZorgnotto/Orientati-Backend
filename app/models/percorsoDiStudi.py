from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class PercorsoDiStudi(Base):
    __tablename__ = "PercorsiDiStudi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    percorsi: Mapped[List["Percorso"]] = relationship("Percorso", back_populates="percorsoDiStudi")  # noqa: F821

    indirizzi: Mapped[List["Indirizzo"]] = relationship(back_populates="percorsoDiStudi")  # noqa: F821
