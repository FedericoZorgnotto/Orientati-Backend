import datetime
import enum

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class CategoriaLogUtente(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogUtente(Base):
    __tablename__ = 'user_action_logs'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    utente_id: Mapped[int] = mapped_column(ForeignKey("Utenti.id"), index=True)
    categoria: Mapped[Enum[CategoriaLogUtente]] = mapped_column(Enum(CategoriaLogUtente), nullable=False,
                                                                default=CategoriaLogUtente.INFO)  # Categoria dell'azione
    azione: Mapped[str] = Column(String, nullable=False)  # Descrizione dell'azione
    dati: Mapped[str] = Column(JSON, nullable=True)  # Dati extra, come parametri
    orario: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now(datetime.UTC),
                                               nullable=False)  # Orario dell'azione
    utente: Mapped["Utente"] = relationship("Utente", back_populates="logs")  # noqa: F821

    def __repr__(self):
        return (f"LogUtente(id={self.id!r}, utente_id={self.utente_id!r}, categoria={self.categoria!r},"
                f" azione={self.azione!r}, dati={self.dati!r}, orario={self.orario!r})")
