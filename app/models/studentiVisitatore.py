from typing import Optional

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class StudenteVisitatore(Base):
    __tablename__ = "studentiVisitatori"

    id: Mapped[int] = mapped_column(primary_key=True)
    Nome: Mapped[str] = mapped_column(String)
    Cognome: Mapped[str] = mapped_column(String)
    ScuolaProvenienza: Mapped[str] = mapped_column(String)
    Presenza: Mapped[bool] = mapped_column(Boolean, default=False)

    percorsoDiStudi_id: Mapped[int] = mapped_column(ForeignKey("percorsiDiStudi.id"))
    percorsoDiStudi: Mapped["PercorsoDiStudi"] = relationship(back_populates="utenti")  # noqa: F821

    indirizzo_id: Mapped[Optional[int]] = mapped_column()
    indirizzo: Mapped[Optional["Indirizzo"]] = relationship(back_populates="studentiVisitatori")  # noqa: F821

    partecipante: Mapped[Optional["Partecipante"]] = relationship(back_populates="studenteVisitatore")  # noqa: F821
