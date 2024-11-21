from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class LogUtenteBase(BaseModel):
    utente_id: Optional[int] = None
    categoria: Optional[str] = None
    azione: Optional[str] = None
    dati: Optional[str] = None
    orario: Optional[str] = None
    utente_nome: Optional[str] = None


class LogUtenteResponse(LogUtenteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LogUtenteDelete(BaseModel):
    id: int


class LogUtenteList(BaseModel):
    logs: List[LogUtenteResponse]
