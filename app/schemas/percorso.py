from typing import Optional

from pydantic import BaseModel


class PercorsoBase(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class PercorsoResponse(PercorsoBase):
    id: int


class PercorsoCreate(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class PercorsoUpdate(BaseModel):
    nome: Optional[str] = None
    percorsoDiStudi_id: Optional[int] = None


class PercorsoDelete(BaseModel):
    id: int


class PercorsoList(BaseModel):
    percorsi: list[PercorsoResponse]
