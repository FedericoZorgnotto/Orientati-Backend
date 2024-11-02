from typing import Optional

from pydantic import BaseModel


class TappaBase(BaseModel):
    percorso_id: int
    aula_id: int
    minuti_arrivo: int
    minuti_partenza: int


class TappaResponse(TappaBase):
    id: int

class TappaCreate(BaseModel):
    percorso_id: int
    aula_id: int
    minuti_arrivo: int
    minuti_partenza: int


class TappaUpdate(BaseModel):
    percorso_id: Optional[int] = None
    aula_id: Optional[int] = None
    minuti_arrivo: Optional[int] = None
    minuti_partenza: Optional[int] = None


class TappaDelete(BaseModel):
    id: int


class TappaList(BaseModel):
    tappe: list[TappaResponse]
