from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.schemas.orientatore.aula import AulaResponse


class TappaBase(BaseModel):
    minuti_arrivo: int
    minuti_partenza: int
    occupata: Optional[bool] = None
    ora_ingresso: Optional[str] = None


class TappaResponse(TappaBase):
    aula: AulaResponse
    model_config = ConfigDict(from_attributes=True)


class TappaList(BaseModel):
    tappe: List[TappaResponse]
