from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.db.database import Base

from src.models.service import tag

class Worker(Base):
    __tablename__ = 'workers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    business: Mapped["Business"] = relationship("Business", back_populates="workers")
    services: Mapped[List["Service"]] = relationship("Service",secondary=tag ,back_populates="workers")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="workers")

