from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Stage(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_minute: Mapped[int]
    end_minute: Mapped[int]

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    route: Mapped["Route"] = relationship(back_populates="stages")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship(back_populates="stages")
