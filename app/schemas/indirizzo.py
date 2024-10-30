from typing import Optional

from pydantic import BaseModel


class IndirizzoBase(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class IndirizzoResponse(IndirizzoBase):
    nomePercorsoDiStudi: str
    id: int


class IndirizzoBaseAdmin(IndirizzoBase):
    id: int


class IndirizzoCreate(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class IndirizzoUpdate(BaseModel):
    nome: Optional[str] = None
    percorsoDiStudi_id: Optional[int] = None


class IndirizzoDelete(BaseModel):
    id: int


class IndirizzoList(BaseModel):
    indirizzi: list[IndirizzoResponse]
