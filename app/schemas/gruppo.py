from typing import Optional

from pydantic import BaseModel


class gruppoBase(BaseModel):
    id: int
    nome: str
    oraPartenza: str
    codice: str

