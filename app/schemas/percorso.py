from typing import List
from pydantic import BaseModel, ConfigDict
from .fasciaOraria import FasciaOrariaBase


class PercorsoBase(BaseModel):
    nome: str
    percorsoDiStudi_id: int
    model_config = ConfigDict(from_attributes=True)


class PercorsoCreate(PercorsoBase):
    pass


class PercorsoUpdate(PercorsoBase):
    pass


class Percorso(PercorsoBase):
    id: int
    fasceOrarie: List[FasciaOrariaBase] = []

    class Config:
        from_attributes = True


class PercorsoList(BaseModel):
    percorsi: List[Percorso]

    class Config:
        from_attributes = True