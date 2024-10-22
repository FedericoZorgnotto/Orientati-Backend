from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Utente(Base):
    __tablename__ = "utenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    # email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    temporaneo: Mapped[bool] = mapped_column(Boolean, default=False)

    codiceGruppo: Mapped["CodiceGruppo"] = relationship(back_populates="utente")  # noqa: F821

    indirizzo_id: Mapped[Optional[int]] = mapped_column()
    indirizzo: Mapped[Optional["Indirizzo"]] = relationship(back_populates="utenti")  # noqa: F821
