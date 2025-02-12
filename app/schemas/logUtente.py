from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class LogUtenteBase(BaseModel):
    utente_id: Optional[int] = None
    categoria: Optional[str] = None
    azione: Optional[str] = None
    dati: Optional[str] = None
    timestamp: Optional[str] = None
    client_ip: Optional[str] = None


class LogUtenteResponse(LogUtenteBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


class LogUtenteDelete(BaseModel):
    id: str


class LogUtenteList(BaseModel):
    logs: List[LogUtenteResponse]
