from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Genitore(Base):
    __tablename__ = "Genitori"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cognome: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column()
    comune: Mapped[str] = mapped_column()

    ragazzi: Mapped[List["Ragazzo"]] = relationship("Ragazzo", back_populates="genitore")  # noqa: F821

    def __repr__(self):
        return (f"Genitore(id={self.id!r}, nome={self.nome!r}, cognome={self.cognome!r}, "
                f"mail={self.mail!r}, comune={self.comune!r})")
