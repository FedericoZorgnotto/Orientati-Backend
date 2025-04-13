from pydantic import BaseModel


class IndirizzoBase(BaseModel):
    nome: str
    percorsoDiStudi_id: int


class IndirizzoCreate(IndirizzoBase):
    pass


class IndirizzoUpdate(IndirizzoBase):
    pass


class Indirizzo(IndirizzoBase):
    id: int

    class Config:
        from_attributes = True