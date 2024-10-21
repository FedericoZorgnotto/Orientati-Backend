from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.models import Gruppo
from .base import Base


class PercorsoDiStudi(Base):
    __tablename__ = "percorsiDiStudi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    gruppi: Mapped[List["Gruppo"]] = relationship()  # noqa: F821