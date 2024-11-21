from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class GruppoBase(BaseModel):
    nome: str
    orario_partenza: str
    numero_tappa: Optional[int] = None
    arrivato: Optional[bool] = None
    nomi_orientatori: Optional[List[str]] = None


class GruppoResponse(GruppoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]
