from datetime import date
from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class LogGruppoTappa(Base):
    __tablename__ = "LogGruppiTappe"
    id: Mapped[int] = mapped_column(primary_key=True)
    oraIngresso: Mapped[str] = mapped_column()
    oraUscita: Mapped[str] = mapped_column()
    tappa_id: Mapped[int] = mapped_column()
    gruppo_id: Mapped[int] = mapped_column()

    tappa: Mapped["Tappa"] = relationship("Tappa", back_populates="logGruppiTappe")  # noqa: F821
    gruppo: Mapped["Gruppo"] = relationship("Gruppo", back_populates="logGruppiTappe")  # noqa: F821

    def __repr__(self):
        return (f"LogGruppoTappa(id={self.id!r}, oraIngresso={self.oraIngresso!r}, "
                f"oraUscita={self.oraUscita!r}, tappa_id={self.tappa_id!r}, "
                f"gruppo_id={self.gruppo_id!r})")