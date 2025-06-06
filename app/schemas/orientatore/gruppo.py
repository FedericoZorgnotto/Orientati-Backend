from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.schemas.orientatore.tappa import TappaResponse


class GruppoBase(BaseModel):
    nome: str
    orario_partenza: str
    gruppo_partito: Optional[bool] = None
    percorso_finito: Optional[bool] = None


class GruppoResponse(GruppoBase):
    tappa: TappaResponse
    tappa_successiva: Optional[TappaResponse] = None
    model_config = ConfigDict(from_attributes=True)


class GruppoResponsePresenze(GruppoResponse):
    orientati_presenti: Optional[int] = None
    orientati_assenti: Optional[int] = None
    orientati_totali: Optional[int] = None


class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]
