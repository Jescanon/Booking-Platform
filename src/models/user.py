from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base

from src.models.booking import Booking
from src.models.business import  Business


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    date_joined: Mapped[datetime] = mapped_column(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    business: Mapped[List["Business"]] = relationship("Business", back_populates="owner")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="user")
