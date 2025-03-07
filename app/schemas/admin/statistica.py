import datetime

from pydantic import BaseModel


class StatisticaBase(BaseModel):
    data: datetime.datetime
    cpu: float
    ram: float


class StatisticaList(BaseModel):
    statistiche: list[StatisticaBase]
