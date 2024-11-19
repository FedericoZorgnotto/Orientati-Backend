from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class OrientatoBase(BaseModel):
    id: int
    nome: str
    cognome: str
    scuolaDiProvenienza_nome: str
    presente: Optional[bool] = None

class OrientatoList(BaseModel):
    orientati: List[OrientatoBase]
