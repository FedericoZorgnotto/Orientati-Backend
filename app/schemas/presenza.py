from pydantic import BaseModel


class PresenteBase(BaseModel):
    ragazzo_id: int
    gruppo_id: int


class PresenteCreate(PresenteBase):
    pass


class PresenteUpdate(PresenteBase):
    pass


class Presente(PresenteBase):
    id: int

    class Config:
        from_attributes = True