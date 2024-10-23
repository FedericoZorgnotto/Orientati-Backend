from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class PercorsoDiStudi(Base):
    __tablename__ = "percorsiDiStudi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    gruppi: Mapped[List["Gruppo"]] = relationship()  # noqa: F821

    indirizzo: Mapped[List["Indirizzo"]] = relationship(back_populates="percorsoDiStudi")  # noqa: F821
