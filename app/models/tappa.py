from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Tappa(Base):
    __tablename__ = "Tappe"

    id: Mapped[int] = mapped_column(primary_key=True)

    percorso_id: Mapped[int] = mapped_column(ForeignKey("Percorsi.id"))
    percorso: Mapped["Percorso"] = relationship("Percorso", back_populates="tappe")  # noqa: F821

    aula_id: Mapped[int] = mapped_column(ForeignKey("Aule.id"))
    aula: Mapped["Aula"] = relationship("Aula", back_populates="tappe")  # noqa: F821
