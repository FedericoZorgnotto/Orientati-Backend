from typing import List

from pydantic import BaseModel


class UpdateBase(BaseModel):
    nome: str
    repo_owner: str = None
    repo_name: str = None
    directory: str = None


class Update(UpdateBase):
    id: int
    aggiornato: bool = True


class UpdateCreate(UpdateBase):
    pass


class UpdateUpdate(UpdateBase):
    pass


class UpdateDelete(BaseModel):
    id: int


class UpdateList(BaseModel):
    updates: List[Update]
