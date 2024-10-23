from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Gruppo(Base):
    __tablename__ = "gruppi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    oraPartenza: Mapped[str] = mapped_column()
    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("percorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship(back_populates="gruppi")  # noqa: F821

    codice: Mapped[str] = mapped_column()

    codiceGruppo: Mapped["CodiceGruppo"] = relationship(back_populates="gruppo")  # noqa: F821

    partecipanti: Mapped[List["Partecipante"]] = relationship(back_populates="gruppo")  # noqa: F821

