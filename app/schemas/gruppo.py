from typing import Optional

from pydantic import BaseModel


class GruppoBase(BaseModel):
    nome: str
    data: str
    orario_partenza: str
    percorso_id: int


class GruppoResponse(GruppoBase):
    id: int


class GruppoCreate(BaseModel):
    nome: str
    data: str
    orario_partenza: str
    percorso_id: int


class GruppoUpdate(BaseModel):
    nome: Optional[str] = None
    data: Optional[str] = None
    orario_partenza: Optional[str] = None
    percorso_id: Optional[int] = None


class GruppoDelete(BaseModel):
    id: int


class GruppoList(BaseModel):
    gruppi: list[GruppoResponse]
