from typing import Optional

from pydantic import ConfigDict, BaseModel


class ScuolaDiProvenienzaBase(BaseModel):
    nome: str
    citta: str


class ScuolaDiProvenienzaBaseAdmin(ScuolaDiProvenienzaBase):
    id: int


class ScuolaDiProvenienzaCreate(BaseModel):
    nome: str
    citta: str


class ScuolaDiProvenienzaUpdate(BaseModel):
    nome: Optional[str] = None
    citta: Optional[str] = None


class ScuolaDiProvenienza(ScuolaDiProvenienzaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ScuolaDiProvenienzaDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ScuolaDiProvenienzaList(BaseModel):
    scuoleDiProvenienza: list[ScuolaDiProvenienza]
    model_config = ConfigDict(from_attributes=True)
