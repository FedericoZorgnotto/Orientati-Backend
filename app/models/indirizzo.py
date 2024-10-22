from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Indirizzo(Base):
    __tablename__ = "indirizzi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

    utenti: Mapped[List["Utente"]] = relationship()  # noqa: F821
