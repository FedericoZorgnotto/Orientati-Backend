from __future__ import annotations

from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base

association_table_orientati = Table(
    "Association_orientati_gruppi",
    Base.metadata,
    Column("idOrientato", ForeignKey("Orientati.id")),
    Column("idGruppo", ForeignKey("Gruppi.id")),
)

association_table_orientatori = Table(
    "Association_orientatori_gruppi",
    Base.metadata,
    Column("idOrientatore", ForeignKey("Orientatori.id")),
    Column("idGruppo", ForeignKey("Gruppi.id")),
)


class Gruppo(Base):
    __tablename__ = "Gruppi"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()

    orientati: Mapped[List["Orientato"]] = relationship(secondary=association_table_orientati,  # noqa: F821
                                                        back_populates="gruppi")

    percorso_id: Mapped[int] = mapped_column(ForeignKey("Percorsi.id"))
    percorso: Mapped["Percorso"] = relationship("Percorso", back_populates="gruppi")  # noqa: F821

    orientatori: Mapped[List["Orientatore"]] = relationship(secondary=association_table_orientatori,  # noqa: F821
                                                            back_populates="gruppi")
