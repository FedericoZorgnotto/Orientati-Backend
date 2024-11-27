from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base
from .gruppo import association_table_orientati


class Orientato(Base):
    __tablename__ = "Orientati"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cognome: Mapped[str] = mapped_column()

    scuolaDiProvenienza_id: Mapped[int] = mapped_column(ForeignKey("ScuoleDiProvenienza.id"))
    scuolaDiProvenienza: Mapped["ScuolaDiProvenienza"] = relationship("ScuolaDiProvenienza",  # noqa: F821
                                                                      back_populates="orientati")

    gruppi: Mapped[List["Gruppo"]] = relationship(  # noqa: F821
        secondary=association_table_orientati, back_populates="orientati"
    )

    presenze: Mapped[List["Presente"]] = relationship("Presente", back_populates="orientato")  # noqa: F821
    assenze: Mapped[List["Assente"]] = relationship("Assente", back_populates="orientato")  # noqa: F821

    def __repr__(self):
        return (f"<Orientato(id={self.id}, nome={self.nome}, cognome={self.cognome}, "
                f"scuolaDiProvenienza_id={self.scuolaDiProvenienza_id}, gruppi={self.gruppi})>")
