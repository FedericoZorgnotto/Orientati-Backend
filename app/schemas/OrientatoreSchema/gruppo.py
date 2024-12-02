from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class GruppoBase(BaseModel):
    nome: str
    data: str
    orario_partenza: str
    percorso_id: int
    numero_tappa: Optional[int] = None
    arrivato: Optional[bool] = None
    percorso_finito: Optional[bool] = None


class GruppoResponse(GruppoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]
