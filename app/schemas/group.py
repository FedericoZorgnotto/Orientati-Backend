from pydantic import ConfigDict, BaseModel


class GroupBase(BaseModel):
    start_hour: str
    stage_number: int = 0
    route_id: int
    is_arrived: bool = False
    notes: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



class GroupUpdate(GroupBase):
    pass


class GroupDelete(GroupBase):
    pass


class GroupRead(GroupBase):
    pass


class GroupList(GroupBase):
    pass
