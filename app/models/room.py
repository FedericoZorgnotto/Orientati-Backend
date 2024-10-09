from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    args: Mapped[str]

    stages: Mapped[List["Stage"]] = relationship(back_populates="room")

    specialisation_id: Mapped[int] = mapped_column(ForeignKey("specialisations.id"))
    specialisation: Mapped["Specialisation"] = relationship(back_populates="rooms")
