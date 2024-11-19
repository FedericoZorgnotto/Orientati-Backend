from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Presente(Base):
    __tablename__ = "Presenti"

    id: Mapped[int] = mapped_column(primary_key=True)

    orientato_id: Mapped[int] = mapped_column(ForeignKey("Orientati.id"))
    gruppo_id: Mapped[int] = mapped_column(ForeignKey("Gruppi.id"))

    orientato: Mapped["Orientato"] = relationship("Orientato", back_populates="presenze")  # noqa: F821

    gruppo: Mapped["Gruppo"] = relationship("Gruppo", back_populates="presenti")  # noqa: F821

    def __repr__(self):
        return f"<Presente(id={self.id}, orientato_id={self.orientato_id}, gruppo_id={self.gruppo_id})>"