from typing import List
from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.db.sesiondb import get_session

from src.models.worker import Worker as WorkerModel
from src.models.user import User as UserModel
from src.models.service import Service as ServiceModel
from src.models.booking import Booking as BookingModel

from src.schemas.booking import CreateBooking, Booking as BookingSchema

from src.core.security import get_current_user


router = APIRouter(prefix="/booking", tags=["booking"])



@router.post("/", response_model=BookingSchema ,status_code=status.HTTP_201_CREATED)
async def create_booking(
        new_booking: CreateBooking,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):
    info_about_service = await db.scalars(select(ServiceModel).where(ServiceModel.id == new_booking.service_id,
                                                                     ServiceModel.is_active == True))
    service = info_about_service.first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Service not found")

    info_about_worker = await db.scalars(select(WorkerModel).where(WorkerModel.id == new_booking.worker_id,
                                                                   WorkerModel.is_active == True))
    worker = info_about_worker.first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Worker not found")

    if worker.id not in [i.id for i in service.workers]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Worker dont provide this service")


    new_bookings = BookingModel(**new_booking.model_dump(), user_id=current_user.id, status="waiting")
    db.add(new_bookings)
    await db.commit()
    await db.refresh(new_bookings)
    return new_bookings


