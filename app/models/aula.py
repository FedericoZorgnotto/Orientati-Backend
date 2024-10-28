from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Aula(Base):
    __tablename__ = "Aule"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    posizione: Mapped[str] = mapped_column()
    materia: Mapped[str] = mapped_column()
    dettagli: Mapped[str] = mapped_column()

    tappe: Mapped[List["Tappa"]] = relationship("Tappa", back_populates="aula")  # noqa: F821
