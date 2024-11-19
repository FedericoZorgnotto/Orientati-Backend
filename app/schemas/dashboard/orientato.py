from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class OrientatoBase(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_nome: str
    presente: Optional[bool] = None


class OrientatoResponse(OrientatoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrientatoList(BaseModel):
    orientati: List[OrientatoBase]
