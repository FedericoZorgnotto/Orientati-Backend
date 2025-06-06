from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class AulaBase(BaseModel):
    nome: str
    posizione: str
    materia: str
    dettagli: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class AulaResponse(AulaBase):
    model_config = ConfigDict(from_attributes=True)


class AulaList(BaseModel):
    aule: List[AulaBase]
