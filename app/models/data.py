from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Data(Base):
    __tablename__ = "Date"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column()

    fasceOrarie: Mapped[List["FasciaOraria"]] = relationship("FasciaOraria", back_populates="data")  # noqa: F821

    def __repr__(self):
        return f"Data(id={self.id!r}, data={self.data!r})"
