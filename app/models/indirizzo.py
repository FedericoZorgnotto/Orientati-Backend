from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .orientatore import Orientatore


class Indirizzo(Base):
    __tablename__ = 'Indirizzi'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    orientatori: Mapped[List[Orientatore]] = relationship('Orientatore', back_populates='indirizzo')

    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("PercorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship('PercorsoDiStudi',  # noqa: F821
                                                              back_populates="indirizzi")
