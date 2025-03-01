from __future__ import annotations

from typing import Optional, List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base

association_ragazzi_iscrizioni = Table(
    "association_ragazzi_iscrizioni",
    Base.metadata,
    Column("ragazzo_id", ForeignKey("Ragazzi.id"), primary_key=True),
    Column("iscrizione_id", ForeignKey("Iscrizioni.id"), primary_key=True),
)


class Iscrizione(Base):
    __tablename__ = "Iscrizioni"

    id: Mapped[int] = mapped_column(primary_key=True)
    gruppo_id: Mapped[Optional[str]] = mapped_column(ForeignKey("Gruppi.id"))
    fasciaOraria_id: Mapped[Optional[str]] = mapped_column(ForeignKey("FasceOrarie.id"))

    ragazzi: Mapped[List["Ragazzo"]] = relationship("Ragazzo", secondary=association_ragazzi_iscrizioni, # noqa: F821
                                                    back_populates="iscrizioni")
    gruppo: Mapped[Optional["Gruppo"]] = relationship("Gruppo", back_populates="iscrizioni")  # noqa: F821
    fasciaOraria: Mapped[Optional["FasciaOraria"]] = relationship("FasciaOraria",  # noqa: F821
                                                                  back_populates="iscrizioni")

    def __repr__(self):
        return f"Iscrizione(id={self.id!r}, gruppo_id={self.gruppo_id!r}, fasciaOraria_id={self.fasciaOraria_id!r})"
