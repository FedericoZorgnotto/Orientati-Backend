from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class AulaBase(BaseModel):
    nome: str
    posizione: str
    materia: str
    dettagli: str
    occupata: Optional[bool] = None
    gruppo_id: Optional[int] = None
    gruppo_nome: Optional[str] = None
    gruppo_orario_partenza: Optional[str] = None


class AulaResponse(AulaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AulaList(BaseModel):
    aule: List[AulaResponse]
