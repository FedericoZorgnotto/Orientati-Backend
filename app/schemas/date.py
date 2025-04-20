from datetime import date
from typing import List

from pydantic import ConfigDict, BaseModel


class PercorsoBase(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class FasciaOrariaBase(BaseModel):
    id: int
    oraInizio: str
    model_config = ConfigDict(from_attributes=True)


class PercorsoConFasce(PercorsoBase):
    fasce: List[FasciaOrariaBase] = []
    model_config = ConfigDict(from_attributes=True)


class DataBase(BaseModel):
    id: int
    data: date
    model_config = ConfigDict(from_attributes=True)


class Data(DataBase):
    percorsi: List[PercorsoConFasce] = []
    model_config = ConfigDict(from_attributes=True)


class DataList(BaseModel):
    date: List[Data]
    model_config = ConfigDict(from_attributes=True)
