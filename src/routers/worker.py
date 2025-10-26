from typing import List
from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.db.sesiondb import get_session

from src.models.worker import Worker as WorkerModel
from src.models.user import User as UserModel
from src.models.business import Business as BusinessModel

from src.schemas.worker import Worker as WorkerSchema, WorkerCreate

from src.core.security import get_current_user, get_current_businessman

from src.utils.generate_linktg import generate_link_token




router = APIRouter(prefix="/worker", tags=["worker"])

@router.post("/workers", response_model=WorkerSchema)
async def register_worker(
    workers: WorkerCreate,
    businessman_owner: UserModel = Depends(get_current_businessman),
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

    exists_worker = await db.scalar(select(WorkerModel.id).where(WorkerModel.user_id == workers.user_id,
                                                                 WorkerModel.business_id == business.id,
                                                                 WorkerModel.is_active == True,
                                                                 ))
    if exists_worker:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Этот пользователь уже работает у вас")

    new_worker = WorkerModel(**workers.model_dump(),
                             business_id=business.id,
                             )

    db.add(new_worker)
    await db.commit()
    await db.refresh(new_worker)
    return new_worker


@router.get("/workers/{business_id}", response_model=List[WorkerSchema])
async def get_workers_in_business(
        business_id: int,
        db: AsyncSession = Depends(get_session),

):
    inf_db = await db.scalars(select(WorkerModel).where(WorkerModel.business_id == business_id,
                                                        WorkerModel.is_active == True))
    information = inf_db.all()
    return information


@router.put("/workers/{worker_id}", response_model=WorkerSchema)
async def update_worker(
        worker_id: int,
        new_worker: WorkerCreate,
        db: AsyncSession = Depends(get_session),
        businessman: UserModel = Depends(get_current_businessman),
):
    information = await db.scalars(select(WorkerModel).where(WorkerModel.id == worker_id,
                                                             WorkerModel.is_active == True))
    inf = information.first()

    if not inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Рабочий не найден")

    if inf.business_id != businessman.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У вас нету доступа к этому рабочим")

    inf_in_user = await db.scalars(select(UserModel).where(UserModel.id == new_worker.user_id,
                                                           UserModel.is_active == True))
    if not inf_in_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пользователь не найден")

    await db.execute(update(WorkerModel).where(WorkerModel.id == worker_id).values(**new_worker.model_dump(),
                                                                                   business_id=businessman.id))

    await db.commit()
    await db.refresh(inf)
    return inf

@router.get("/workers", response_model=List[WorkerSchema])
async def get_workers(current_businessman: UserModel = Depends(get_current_businessman),
                      db: AsyncSession = Depends(get_session)
                      ):

    res = await db.scalars(select(WorkerModel).where(WorkerModel.business_id == current_businessman.id,
                                                     WorkerModel.is_active == True))
    result = res.all()
    return result


@router.put("/register_telegram")
async def register_telegram(db: AsyncSession = Depends(get_session),
                            current_user: UserModel = Depends(get_current_user)):

    info = await db.scalars(select(WorkerModel).where(WorkerModel.user_id == current_user.id,
                                                      WorkerModel.is_active == True))

    res = info.first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого работника нету, или вы не зарегистрированы как работник")

    if res.telegram_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вы уже привязали свой телеграм")

    link_tg = await generate_link_token(current_user.id, db)

    return {"link": f"https://t.me/bk_push_info_bot?start={link_tg}"}
