from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.models import Indirizzo
from .base import Base

association_ragazzi_indirizzi = Table(
    "association_ragazzi_indirizzi",
    Base.metadata,
    Column("ragazzo_id", ForeignKey("Ragazzi.id")),
    Column("indirizzoDiInteresse_id", ForeignKey("Indirizzi.id")),
)


class Ragazzo(Base):
    __tablename__ = "Ragazzi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cognome: Mapped[str] = mapped_column()
    scuolaDiProvenienza_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ScuoleDiProvenienza.id"))
    genitore_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Genitori.id"))

    scuolaDiProvenienza: Mapped[Optional["Scuola"]] = relationship("ScuolaDiProvenienza",  # noqa: F821
                                                                   back_populates="ragazzi")
    genitore: Mapped[Optional["Genitore"]] = relationship("Genitore", back_populates="ragazzi")  # noqa: F821

    iscrizioni: Mapped[List["Iscrizione"]] = relationship("Iscrizione",  # noqa: F821
                                                          secondary="association_ragazzi_iscrizioni",
                                                          back_populates="ragazzi")
    presenze: Mapped[List["Presente"]] = relationship("Presente", back_populates="ragazzo")  # noqa: F821
    assenze: Mapped[List["Assente"]] = relationship("Assente", back_populates="ragazzo")  # noqa: F821

    indirizziDiInteresse: Mapped[List["Indirizzo"]] = relationship("Indirizzo", secondary=association_ragazzi_indirizzi,
                                                                   back_populates="ragazziInteressati")

    def __repr__(self):
        return (f"Ragazzo(id={self.id!r}, nome={self.nome!r}, cognome={self.cognome!r}, "
                f"scuolaDiProvenienza_id={self.scuolaDiProvenienza_id!r}, genitore_id={self.genitore_id!r}, "
                f"indirizziDiInteresse={self.indirizziDiInteresse!r})")