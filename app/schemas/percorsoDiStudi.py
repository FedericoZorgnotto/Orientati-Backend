from typing import Optional

from pydantic import ConfigDict, BaseModel


class PercorsoDiStudiBase(BaseModel):
    nome: str


class PercorsoDiStudiBaseAdmin(PercorsoDiStudiBase):
    id: int


class PercorsoDiStudiCreate(BaseModel):
    nome: str


class PercorsoDiStudiUpdate(BaseModel):
    nome: Optional[str] = None


class PercorsoDiStudi(PercorsoDiStudiBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PercorsoDiStudiDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PercorsoDiStudiList(BaseModel):
    percorsiDiStudi: list[PercorsoDiStudi]
    model_config = ConfigDict(from_attributes=True)
