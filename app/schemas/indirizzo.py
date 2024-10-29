from typing import Optional

from pydantic import ConfigDict, BaseModel


class IndirizzoBase(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class IndirizzoBaseAdmin(IndirizzoBase):
    id: int


class IndirizzoCreate(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class IndirizzoUpdate(BaseModel):
    nome: Optional[str] = None
    percorsoDiStudi_id: Optional[int] = None


class Indirizzo(IndirizzoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class IndirizzoDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class IndirizzoList(BaseModel):
    indirizzi: list[Indirizzo]
    model_config = ConfigDict(from_attributes=True)
