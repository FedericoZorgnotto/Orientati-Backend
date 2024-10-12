from pydantic import ConfigDict, BaseModel


class GroupBase(BaseModel):
    start_hour: str
    notes: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    route_id: int
    model_config = ConfigDict(from_attributes=True)
    stage_number: int
    is_arrived: bool


class GroupUpdate(GroupBase):
    pass


class GroupDelete(GroupBase):
    pass


class GroupRead(GroupBase):
    pass


class GroupList(GroupBase):
    pass
