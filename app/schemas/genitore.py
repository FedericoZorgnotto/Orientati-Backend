from typing import List

from pydantic import BaseModel, EmailStr


class GenitoreBase(BaseModel):
    nome: str
    cognome: str
    email: str
    comune: str


class GenitoreCreate(GenitoreBase):
    pass


class Genitore(GenitoreBase):
    id: int

    class Config:
        from_attributes = True


class GenitoreLogin(Genitore):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class GenitoreWithRagazzi(Genitore):
    ragazzi: List["Ragazzo"]  # noqa: F821

    class Config:
        from_attributes = True


class EmailSchema(BaseModel):
    email: EmailStr


class GenitoreUpdate(BaseModel):
    email: EmailStr
    nome: str
    cognome: str
    comune: str
