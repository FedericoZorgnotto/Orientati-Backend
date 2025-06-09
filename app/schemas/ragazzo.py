from typing import List

from pydantic import BaseModel

from .assenza import Assente
from .indirizzo import Indirizzo
from .presenza import Presente


class RagazzoBase(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int | None = None
    genitore_id: int | None = None


class RagazzoCreate(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int
    indirizziDiInteresse: List[int] = []


class RagazzoUpdate(BaseModel):
    nome: str | None = None
    cognome: str | None = None
    scuolaDiProvenienza_id: int | None = None


class Ragazzo(RagazzoBase):
    id: int
    iscrizioni: List["Iscrizione"] = []
    presenze: List[Presente] = []
    assenze: List[Assente] = []
    indirizziDiInteresse: List[Indirizzo] = []

    class Config:
        from_attributes = True


class RagazzoList(BaseModel):
    ragazzi: List[Ragazzo]

    class Config:
        from_attributes = True


from app.schemas.iscrizione import Iscrizione  # noqa: E402

Ragazzo.model_rebuild()
