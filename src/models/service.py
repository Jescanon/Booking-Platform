from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Table, Column

from src.db.database import Base

from src.models.booking import Booking
from src.models.business import  Business
from src.models.worker import Worker

tag = Table(
    'tag',
    Base.metadata,
    Column('workers_id', ForeignKey("workers.id"), primary_key=True),
    Column('services_id',ForeignKey("services.id"), primary_key=True),
)

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float]

    business: Mapped["Business"] = relationship("Business", back_populates="services")
    workers: Mapped[List["Worker"]] = relationship("Worker", secondary=tag,back_populates="services")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="services")



