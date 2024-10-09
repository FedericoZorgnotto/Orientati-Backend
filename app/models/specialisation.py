from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Specialisation(Base):
    __tablename__ = "specialisations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    users: Mapped[List['User']] = relationship(back_populates="specialisation")
    rooms: Mapped[List['Room']] = relationship(back_populates="specialisation")
