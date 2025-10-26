from typing import List
from datetime import timezone
from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, Table

from src.db.sesiondb import get_session

from src.models.worker import Worker as WorkerModel
from src.models.user import User as UserModel
from src.models.service import Service as ServiceModel
from src.models.booking import Booking as BookingModel
from src.models.service import tag


from src.schemas.booking import CreateBooking, Booking as BookingSchema

from src.core.security import get_current_user

from src.tasks.send_message_tg import send_message_tg



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
                            detail="Сервис не найден")

    info_about_worker = await db.scalars(select(WorkerModel).where(WorkerModel.id == new_booking.worker_id,
                                                                   WorkerModel.is_active == True))
    worker = info_about_worker.first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Воркер не найден")

    res = await db.scalars(select(tag).where(tag.workers_id == new_booking.worker_id,
                                             tag.services_id == new_booking.service_id))

    if not res.first():
        raise HTTPException(status_code=404,
                            detail="Воркер не выполняет данную услугу")


    new_booking.start_time = new_booking.start_time.astimezone(timezone.utc).replace(tzinfo=None)
    new_bookings = BookingModel(**new_booking.model_dump(), user_id=current_user.id, status="waiting")

    send_message_tg.apply_async(args=[{
        "worker_name": worker.name,
        "worker_telegram_id": worker.telegram_id,
        "start_time": new_bookings.start_time.isoformat(),
        "user_id": current_user.id
    }])

    db.add(new_bookings)
    await db.commit()
    await db.refresh(new_bookings)
    return new_bookings


@router.get("/booking", response_model=List[BookingSchema], status_code=status.HTTP_200_OK)
async def get_all_bookings(db: AsyncSession = Depends(get_session),
                           current_user: UserModel = Depends(get_current_user),):
    db_bookings = await db.scalars(select(BookingModel).where(BookingModel.user_id == current_user.id,
                                                              BookingModel.start_time == "waiting",))

    return db_bookings.all()

