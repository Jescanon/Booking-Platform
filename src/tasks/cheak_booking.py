from datetime import datetime, timezone
from celery import shared_task

from sqlalchemy import update

from src.db.database import session_factory
from src.models.booking import Booking as BookingModel

from asyncio import run




@shared_task()
def event_loop():

    async def check_booking():

        async with session_factory() as db:

            await db.execute(update(BookingModel).where(BookingModel.start_time < datetime.now(timezone.utc),
                                                               BookingModel.status == "waiting").values(status="end"))
            await db.commit()

    run(check_booking())