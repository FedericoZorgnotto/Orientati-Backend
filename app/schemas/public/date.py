from pydantic import ConfigDict, BaseModel
from typing import List, Optional


class PercorsoBase(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class FasciaOrariaBase(BaseModel):
    id: int
    oraInizio: str
    percorso_id: int
    model_config = ConfigDict(from_attributes=True)


class FasciaOraria(FasciaOrariaBase):
    percorso: PercorsoBase
    model_config = ConfigDict(from_attributes=True)


class DataBase(BaseModel):
    id: int
    data: str
    model_config = ConfigDict(from_attributes=True)


class Data(DataBase):
    fasceOrarie: List[FasciaOraria] = []
    model_config = ConfigDict(from_attributes=True)


class DataList(BaseModel):
    date: List[Data]
    model_config = ConfigDict(from_attributes=True)