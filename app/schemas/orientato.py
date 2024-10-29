from typing import Optional

from pydantic import ConfigDict, BaseModel


class OrientatoBase(BaseModel):
    nome: str
    cognome: str
    scuolediprovenienza_id: int


class OrientatoBaseAdmin(OrientatoBase):
    id: int


class OrientatoCreate(BaseModel):
    nome: str
    cognome: str


class OrientatoUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    scuolediprovenienza_id: Optional[int] = None


class Orientato(OrientatoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrientatoDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrientatoList(BaseModel):
    orientati: list[Orientato]
    model_config = ConfigDict(from_attributes=True)
