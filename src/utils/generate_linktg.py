import uuid

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.worker import Worker as WorkerModel

async def generate_link_token(user_id, db: AsyncSession):
    token = str(uuid.uuid4())

    await db.execute(update(WorkerModel).where(WorkerModel.user_id == user_id).values(link_token=token))
    await db.commit()

    return token
