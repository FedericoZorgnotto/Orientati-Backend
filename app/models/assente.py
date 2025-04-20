from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Assente(Base):
    __tablename__ = "Assenti"

    id: Mapped[int] = mapped_column(primary_key=True)

    ragazzo_id: Mapped[int] = mapped_column(ForeignKey("Ragazzi.id"))
    gruppo_id: Mapped[int] = mapped_column(ForeignKey("Gruppi.id"))

    ragazzo: Mapped["Ragazzo"] = relationship("Ragazzo", back_populates="assenze")  # noqa: F821

    gruppo: Mapped["Gruppo"] = relationship("Gruppo", back_populates="assenti")  # noqa: F821

    def __repr__(self):
        return f"<Assente(id={self.id}, ragazzo_id={self.ragazzo_id}, gruppo_id={self.gruppo_id})>"
