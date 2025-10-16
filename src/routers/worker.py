from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sesiondb import get_session

from src.models.worker import Worker as WorkerModel
from src.models.user import User as UserModel
from src.models.business import Business as BusinessModel

from src.schemas.worker import Worker as WorkerSchema, WorkerCreate

from src.core.security import get_current_user, get_current_businessman

from src.models import User

from sqlalchemy import select


router = APIRouter(prefix="/worker", tags=["worker"])

@router.post("/workers", response_model=WorkerSchema)
async def register_worker(
    workers: WorkerCreate,
    businessman_owner: User = Depends(get_current_businessman),
    db: AsyncSession = Depends(get_session)
):

    business = await db.scalar(
        select(BusinessModel)
        .where(BusinessModel.owner_id == businessman_owner.id, BusinessModel.is_active == True)
    )
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ваш бизнес не найден")


    user = await db.scalar(
        select(UserModel)
        .where(UserModel.id == workers.user_id, UserModel.is_active == True)
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    exists_worker = await db.scalar(
        select(WorkerModel.id).where(
            WorkerModel.user_id == workers.user_id,
            WorkerModel.business_id == business.id,
            WorkerModel.is_active == True
        )
    )
    if exists_worker:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Этот пользователь уже работает у вас")

    new_worker = WorkerModel(**workers.model_dump(), business_id=business.id)

    db.add(new_worker)
    await db.commit()
    await db.refresh(new_worker)
    return new_worker


