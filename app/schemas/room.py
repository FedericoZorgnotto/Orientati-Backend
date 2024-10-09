from pydantic import ConfigDict, BaseModel


class RoomBase(BaseModel):
    name: str
    args: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    specialisation_id: int
    model_config = ConfigDict(from_attributes=True)


class RoomUpdate(RoomBase):
    pass


class RoomDelete(RoomBase):
    id: int
    specialisation_id: int
    model_config = ConfigDict(from_attributes=True)


class RoomRead(RoomBase):
    id: int
    specialisation_id: int
    model_config = ConfigDict(from_attributes=True)


class RoomReadAll(RoomBase):
    id: int
    specialisation_id: int
    model_config = ConfigDict(from_attributes=True)
