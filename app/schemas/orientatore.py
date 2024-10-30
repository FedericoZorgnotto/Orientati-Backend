from typing import Optional

from pydantic import ConfigDict, BaseModel


class OrientatoreBase(BaseModel):
    nome: str
    cognome: str
    email: str
    classe: str
    indirizzo_id: int
    gruppi: list[int]


class OrientatoreResponse(OrientatoreBase):
    nomeIndirizzo: str
    id: int


class OrientatoreBaseAdmin(OrientatoreBase):
    id: int


class OrientatoreCreate(BaseModel):
    nome: str
    cognome: str
    email: str
    classe: str
    indirizzo_id: int


class OrientatoreUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    email: Optional[str] = None
    classe: Optional[str] = None
    indirizzo_id: Optional[int] = None


class OrientatoreDelete(BaseModel):
    id: int


class OrientatoreList(BaseModel):
    orientatori: list[OrientatoreResponse]
    model_config = ConfigDict(from_attributes=True)
