from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class FasciaOraria(Base):
    __tablename__ = "FasceOrarie"

    id: Mapped[int] = mapped_column(primary_key=True)
    data_id: Mapped[int] = mapped_column(ForeignKey("Date.id"))
    oraInizio: Mapped[str] = mapped_column()
    percorso_id: Mapped[int] = mapped_column(ForeignKey("Percorsi.id"))

    data: Mapped["Data"] = relationship("Data", back_populates="fasceOrarie")  # noqa: F821
    percorso: Mapped["Percorso"] = relationship("Percorso", back_populates="fasceOrarie")  # noqa: F821

    iscrizioni: Mapped["Iscrizione"] = relationship("Iscrizione", back_populates="fasciaOraria")  # noqa: F821

    def __repr__(self):
        return (f"FasciaOraria(id={self.id!r}, data_id={self.data_id!r}, oraInizio={self.oraInizio!r}, "
                f"percorso_id={self.percorso_id!r})")
