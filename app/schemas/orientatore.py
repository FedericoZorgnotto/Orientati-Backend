from typing import Optional

from pydantic import ConfigDict, BaseModel


class OrientatoreBase(BaseModel):
    nome: str
    cognome: str
    indirizzo_id: int
    gruppi: list[int]


class OrientatoreBaseAdmin(OrientatoreBase):
    id: int


class OrientatoreCreate(BaseModel):
    nome: str
    cognome: str
    indirizzo_id: int

class OrientatoreUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    indirizzo_id: Optional[int] = None


class Orientatore(OrientatoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrientatoreDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrientatoreList(BaseModel):
    orientatori: list[Orientatore]
    model_config = ConfigDict(from_attributes=True)
