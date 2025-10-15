from typing import List

from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql.functions import current_user

from src.db.sesiondb import get_session
from src.models import User

from src.models.business import Business as BusinessModel
from src.models.user import User as UserModel

from src.schemas.business import Business as BusinessSchema, CreateBusiness

from src.core.security import hashed_password, verify_password, create_access_token, get_current_user, get_current_businessman


router = APIRouter(prefix="/business", tags=["business"])


@router.get("/", response_model=List[BusinessSchema])
async def read_business(db: AsyncSession = Depends(get_session)):
    inf_on_db = await db.scalars(select(BusinessModel).where(BusinessModel.is_active == True))
    return inf_on_db.all()


@router.post("/create_business", response_model=BusinessSchema)
async def create_business(info_business: CreateBusiness, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):

    info = await db.scalars(select(BusinessModel).where(BusinessModel.name == info_business.name, BusinessModel.is_active == True))
    if info.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бизнес с таким именем занят")


    model_bus = BusinessModel(**info_business.model_dump(), owner_id=current_user.id)

    db.add(model_bus)
    await db.execute(update(UserModel).where(UserModel.id == current_user.id).values(role="businessman"))
    await db.commit()

    return model_bus

@router.get("/update_business", response_model=List[BusinessSchema])
async def get_all_my_business(db: AsyncSession = Depends(get_session), current_bus: User = Depends(get_current_businessman)):
    inf = await db.scalars(select(BusinessModel).where(BusinessModel.is_active == True, BusinessModel.owner_id == current_bus.id))
    return inf.all()

@router.put("/update_business/{business_id}", response_model=BusinessSchema)
async def change_business(business_id: int,
                          new_business: CreateBusiness,
                          db: AsyncSession = Depends(get_session),
                          current_bus: User = Depends(get_current_businessman)):

    inf_in_db = await db.scalars(select(BusinessModel).where(BusinessModel.is_active == True, BusinessModel.id == business_id))
    inf = inf_in_db.first()

    if not inf or inf.owner_id != current_bus.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Business not found")

    await db.execute(update(BusinessModel).where(BusinessModel.id == business_id).values(**new_business.model_dump(), owner_id=current_bus.id))
    await db.commit()
    await db.refresh(inf)
    return inf

@router.delete("/delete_business/{business_id}")
async def delete_business(business_id: int,
                          db: AsyncSession = Depends(get_session),
                          current_bus: User = Depends(get_current_businessman)):

    inf_in_db = await db.scalars(select(BusinessModel).where(BusinessModel.is_active == True, BusinessModel.id == business_id))
    inf = inf_in_db.first()

    if not inf or inf.owner_id != current_bus.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя удалать чужой бизнесс")

    await db.execute(update(BusinessModel).where(BusinessModel.id == business_id).values(is_active = False))
    await db.commit()
    await db.refresh(inf)
    return {"success": "Удалили"}

