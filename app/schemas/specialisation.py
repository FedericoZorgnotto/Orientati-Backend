from pydantic import ConfigDict, BaseModel


class SpecialisationBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class SpecialisationCreate(SpecialisationBase):
    pass


class SpecialisationUpdate(SpecialisationBase):
    pass


class Specialisation(SpecialisationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SpecialisationDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SpecialisationList(BaseModel):
    specialisations: list[Specialisation]
    model_config = ConfigDict(from_attributes=True)
