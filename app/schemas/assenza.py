from pydantic import BaseModel


class AssenteBase(BaseModel):
    ragazzo_id: int
    gruppo_id: int


class AssenteCreate(AssenteBase):
    pass


class AssenteUpdate(AssenteBase):
    pass


class Assente(AssenteBase):
    id: int

    class Config:
        from_attributes = True