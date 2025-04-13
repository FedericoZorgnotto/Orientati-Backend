from typing import Optional

from pydantic import BaseModel


class IscrizioneBase(BaseModel):
    gruppo_id: Optional[str] = None
    fasciaOraria_id: Optional[str] = None


class IscrizioneCreate(IscrizioneBase):
    pass


class IscrizioneUpdate(IscrizioneBase):
    pass


class Iscrizione(IscrizioneBase):
    id: int

    class Config:
        from_attributes = True
