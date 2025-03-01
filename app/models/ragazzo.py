from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Ragazzo(Base):
    __tablename__ = "Ragazzi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cognome: Mapped[str] = mapped_column()
    scuolaDiProvenienza_id: Mapped[int] = mapped_column(ForeignKey("ScuoleDiProvenienza.id"))
    genitore_id: Mapped[str] = mapped_column(ForeignKey("Genitori.id"))
    indirizzoDiInteresse_1_id: Mapped[int] = mapped_column(ForeignKey("Indirizzi.id"))
    indirizzoDiInteresse_2_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Indirizzi.id"))
    indirizzoDiInteresse_3_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Indirizzi.id"))

    scuolaDiProvenienza: Mapped["Scuola"] = relationship("ScuolaDiProvenienza", back_populates="ragazzi")  # noqa: F821
    genitore: Mapped["Genitore"] = relationship("Genitore", back_populates="ragazzi")  # noqa: F821

    indirizzoDiInteresse_1: Mapped["Indirizzo"] = relationship("Indirizzo", back_populates="ragazzi")  # noqa: F821
    indirizzoDiInteresse_2: Mapped[Optional["Indirizzo"]] = relationship("Indirizzo",  # noqa: F821
                                                                         back_populates="ragazzi")
    indirizzoDiInteresse_3: Mapped[Optional["Indirizzo"]] = relationship("Indirizzo",  # noqa: F821
                                                                         back_populates="ragazzi")

    iscrizioni: Mapped[List["Iscrizione"]] = relationship("Iscrizione", back_populates="ragazzi")  # noqa: F821
    presenze: Mapped[List["Presente"]] = relationship("Presente", back_populates="ragazzo")  # noqa: F821
    assenze: Mapped[List["Assente"]] = relationship("Assente", back_populates="ragazzo")  # noqa: F821

    def __repr__(self):
        return (f"Ragazzo(id={self.id!r}, nome={self.nome!r}, cognome={self.cognome!r}, "
                f"scuolaDiProvenienza_id={self.scuolaDiProvenienza_id!r}, genitore_id={self.genitore_id!r}, "
                f"indirizzoDiInteresse_1_id={self.indirizzoDiInteresse_1_id!r}, "
                f"indirizzoDiInteresse_2_id={self.indirizzoDiInteresse_2_id!r}, "
                f"indirizzoDiInteresse_3_id={self.indirizzoDiInteresse_3_id!r})")
