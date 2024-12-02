from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Indirizzo(Base):
    __tablename__ = 'Indirizzi'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("PercorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship('PercorsoDiStudi',  # noqa: F821
                                                              back_populates="indirizzi")

    def __repr__(self):
        return f"Indirizzo(id={self.id!r}, nome={self.nome!r}, percorsoDiStudi_id={self.percorsoDiStudi_id!r})"
