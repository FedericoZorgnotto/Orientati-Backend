from pydantic import ConfigDict, BaseModel


class StageBase(BaseModel):
    start_minute: int
    end_minute: int
    route_id: int
    room_id: int
    model_config = ConfigDict(from_attributes=True)


class StageCreate(StageBase):
    pass


class StageUpdate(StageBase):
    pass


class Stage(StageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StageDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StageList(BaseModel):
    stages: list[Stage]
    model_config = ConfigDict(from_attributes=True)
