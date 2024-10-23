from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Indirizzo(Base):
    __tablename__ = "indirizzi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("percorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship(back_populates="indirizzo")  # noqa: F821

    utenti: Mapped[List["Utente"]] = relationship()  # noqa: F821
    studentiInteressati: Mapped[List["StudenteVisitatore"]] = relationship(back_populates="indirizzo")  # noqa: F821
