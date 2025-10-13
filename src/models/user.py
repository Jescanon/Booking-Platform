from datetime import datetime, timezone
from typing import List

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base



class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default='user')
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc), nullable=False)

    business: Mapped[List["Business"]] = relationship("Business", back_populates="owner")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="user")
