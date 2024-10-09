from typing import Optional

from pydantic import ConfigDict, BaseModel


class RouteBase(BaseModel):
    name: str


class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RouteUpdate(RouteBase):
    name: Optional[str] = None


class RouteDelete(RouteBase):
    model_config = ConfigDict(from_attributes=True)


class RouteRead(RouteBase):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class RouteReadAll(RouteBase):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
