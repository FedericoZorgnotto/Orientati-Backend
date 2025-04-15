from typing import List

from pydantic import BaseModel


class ScuolaDiProvenienzaBase(BaseModel):
    nome: str
    citta: str
    isUfficiale: bool


class ScuolaDiProvenienzaCreate(ScuolaDiProvenienzaBase):
    pass


class ScuolaDiProvenienza(ScuolaDiProvenienzaBase):
    id: int

    class Config:
        from_attributes = True


class ScuolaDiProvenienzaList(BaseModel):
    scuole: List[ScuolaDiProvenienza]