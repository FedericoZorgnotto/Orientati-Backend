from typing import List

from pydantic import BaseModel

from .assenza import Assente
from .indirizzo import Indirizzo
from .iscrizione import Iscrizione
from .presenza import Presente


class RagazzoBase(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int
    genitore_id: int


class RagazzoCreate(RagazzoBase):
    pass


class RagazzoUpdate(RagazzoBase):
    pass


class Ragazzo(RagazzoBase):
    id: int
    iscrizioni: List[Iscrizione] = []
    presenze: List[Presente] = []
    assenze: List[Assente] = []
    indirizziDiInteresse: List[Indirizzo] = []

    class Config:
        from_attributes = True


class RagazzoList(BaseModel):
    ragazzi: List[Ragazzo]

    class Config:
        from_attributes = True
