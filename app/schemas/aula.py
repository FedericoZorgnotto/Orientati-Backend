from typing import Optional

from pydantic import BaseModel


class AulaBase(BaseModel):
    nome: str
    posizione: str
    materia: str
    dettagli: str


class AulaResponse(AulaBase):
    id: int


class AulaCreate(BaseModel):
    nome: str
    posizione: str
    materia: str
    dettagli: str


class AulaUpdate(BaseModel):
    nome: Optional[str] = None
    posizione: Optional[str] = None
    materia: Optional[str] = None
    dettagli: Optional[str] = None


class AulaDelete(BaseModel):
    id: int


class AulaList(BaseModel):
    aule: list[AulaResponse]
