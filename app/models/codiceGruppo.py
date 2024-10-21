from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class CodiceGruppo(Base):
    __tablename__ = "codiciGruppi"

    id: Mapped[int] = mapped_column(primary_key=True)

    utente_id: Mapped[int] = mapped_column(ForeignKey("utenti.id"))
    gruppo_id: Mapped[int] = mapped_column(ForeignKey("gruppi.id"))

    utente: Mapped["Utente"] = relationship(back_populates="codiceGruppo")  # noqa: F821
    gruppo: Mapped["Gruppo"] = relationship(back_populates="codiceGruppo")  # noqa: F821
