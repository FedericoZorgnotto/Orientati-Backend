from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_hour: Mapped[str]
    notes: Mapped[str]
    stage_number: Mapped[Optional[int]] = mapped_column()
    is_arrived: Mapped[Optional[bool]] = mapped_column()

    users: Mapped[List["User"]] = relationship(back_populates="group")

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    route: Mapped["Route"] = relationship(back_populates="groups")
