from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Partecipante(Base):
    __tablename__ = "partecipanti"

    id: Mapped[int] = mapped_column(primary_key=True)

    studenteVisitatore_id: Mapped[int] = mapped_column(ForeignKey("studentiVisitatori.id"))
    studenteVisitatore: Mapped["StudenteVisitatore"] = relationship(back_populates="partecipante")  # noqa: F821

    gruppo_id: Mapped[int] = mapped_column(ForeignKey("gruppi.id"))
    gruppo: Mapped["Gruppo"] = relationship(back_populates="partecipanti")  # noqa: F821
