from typing import Optional

from pydantic import BaseModel


class TappaBase(BaseModel):
    percorso_id: int
    aula_id: int
    minuti_arrivo: int
    minuti_partenza: int
    aula_nome: str
    aula_posizione: str
    aula_materia: str


class TappaResponse(TappaBase):
    id: int

class TappaList(BaseModel):
    tappe: list[TappaResponse]
