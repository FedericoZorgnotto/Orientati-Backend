from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class ScuolaDiProvenienza(Base):
    __tablename__ = "ScuoleDiProvenienza"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    citta: Mapped[str] = mapped_column()
    isUfficiale: Mapped[bool] = mapped_column(default=True, nullable=False)

    ragazzi: Mapped[List["Ragazzo"]] = relationship("Ragazzo", back_populates="scuolaDiProvenienza")  # noqa: F821

    def __repr__(self):
        return f"ScuolaDiProvenienza(id={self.id!r}, nome={self.nome!r}, citta={self.citta!r})"
