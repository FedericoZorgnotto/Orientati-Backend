from typing import Optional, List

from pydantic import BaseModel


class OrientatoBase(BaseModel):
    id: int
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int | None = None
    scuolaDiProvenienza_nome: str | None = None
    presente: Optional[bool] = None
    assente: Optional[bool] = None


class OrientatiStatisticheResponse(BaseModel):
    totali: int
    presenti: int
    assenti: int


class OrientatoCreate(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int
    gruppo_id: int


class OrientatoList(BaseModel):
    orientati: List[OrientatoBase]


class IscrizioneBase(BaseModel):
    genitore_id: int | None = None
    genitore_nome: str | None = None
    genitore_cognome: str | None = None
    fascia_oraria_id: int | None = None
    gruppo_id: int
    gruppo_nome: str
    gruppo_orario_partenza: str
    orientati: List[OrientatoBase] = []


class IscrizioneList(BaseModel):
    iscrizioni: List[IscrizioneBase]
