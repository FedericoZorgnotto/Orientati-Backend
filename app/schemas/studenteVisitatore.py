from typing import Optional

from pydantic import ConfigDict, BaseModel


class StudenteVisitatoreBase(BaseModel):
    id: int
    nome: str
    cognome: str
    scuolaProvenienza: str
    presenza: bool

    indirizzo_di_interesse_id: int


class StudenteVisitatoreList(StudenteVisitatoreBase):
    studenti: list[StudenteVisitatoreBase] = []
    model_config = ConfigDict(from_attributes=True)


class StudenteVisitatoreCreate(StudenteVisitatoreBase):
    nome: str
    cognome: str
    scuolaProvenienza: str
    presenza: Optional[bool] = False

    indirizzo_di_interesse_id: Optional[int] = None


class StudenteVisitatoreUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    scuolaProvenienza: Optional[str] = None
    presenza: Optional[bool] = None

    indirizzo_di_interesse_id: Optional[int] = None


class StudenteVisitatoreDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StudenteVisitatoreBaseAdmin(StudenteVisitatoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
