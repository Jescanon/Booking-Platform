from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.db.database import Base

from src.models.user import User
from src.models.service import Service
from src.models.worker import Worker


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'), nullable=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'), nullable=False)

    start_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="bookings")
    services: Mapped["Service"] = relationship("Service", back_populates="bookings")
    workers: Mapped["Worker"] = relationship("Worker", back_populates="bookings")
