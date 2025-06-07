from typing import List, Optional, ForwardRef

from pydantic import BaseModel

DataBase = ForwardRef('DataBase')


class FasciaOrariaBase(BaseModel):
    data_id: int
    oraInizio: str
    percorso_id: int


class FasciaOrariaCreate(FasciaOrariaBase):
    pass


class FasciaOraria(FasciaOrariaBase):
    id: int
    percorso: Optional["PercorsoBase"]  # noqa: F821
    data: Optional[DataBase]

    class Config:
        from_attributes = True


class FasciaOrariaList(BaseModel):
    fasce_orarie: List["FasciaOraria"]

    class Config:
        from_attributes = True


from .date import DataBase
from .percorso import PercorsoBase
