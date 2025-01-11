from typing import Optional, List

from pydantic import BaseModel


class OrientatoBase(BaseModel):
    id: int
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int
    scuolaDiProvenienza_nome: str
    gruppo_id: Optional[int] = None
    gruppo_nome: str
    gruppo_orario_partenza: str
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
