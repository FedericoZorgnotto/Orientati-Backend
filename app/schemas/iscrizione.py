from typing import Optional, List, ForwardRef
from pydantic import BaseModel

# Forward references
FasciaOraria = ForwardRef('FasciaOraria')
Ragazzo = ForwardRef('RagazzoBase')

class IscrizioneBase(BaseModel):
    gruppo_id: Optional[int] = None
    fasciaOraria_id: Optional[int] = None

class IscrizioneCreate(IscrizioneBase):
    ragazzi_id: List[int]

class IscrizioneUpdate(IscrizioneBase):
    pass

class Iscrizione(IscrizioneBase):
    id: int
    fasciaOraria: Optional[FasciaOraria]
    ragazzi: List[Ragazzo]

    class Config:
        from_attributes = True

class IscrizioneList(BaseModel):
    iscrizioni: List[Iscrizione]

    class Config:
        from_attributes = True

# Import at the bottom after all class definitions
from app.schemas.fasciaOraria import FasciaOraria
from app.schemas.ragazzo import RagazzoBase
