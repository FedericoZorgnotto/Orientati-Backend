from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Percorso(Base):
    __tablename__ = "Percorsi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    gruppi: Mapped[List["Gruppo"]] = relationship("Gruppo", back_populates="percorso")  # noqa: F821

    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("PercorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship("PercorsoDiStudi",  # noqa: F821
                                                              back_populates="percorsi")

    tappe: Mapped[List["Tappa"]] = relationship("Tappa", back_populates="percorso")  # noqa: F821
    fasceOrarie: Mapped[List["FasciaOraria"]] = relationship("FasciaOraria",  # noqa: F821
                                                              back_populates="percorso")
    def __repr__(self):
        return f"Percorso(id={self.id!r}, nome={self.nome!r}, percorsoDiStudi_id={self.percorsoDiStudi_id!r})"
