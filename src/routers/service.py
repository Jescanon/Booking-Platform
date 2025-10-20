from typing import List

from fastapi import HTTPException, status, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sesiondb import get_session

from src.models.business import Business as BusinessModel
from src.models.service import Service as ServiceModel
from src.models.user import User as UserModel

from src.schemas.service import ServiceCreat, Service  as ServiceSchema

from src.core.security import get_current_businessman

from sqlalchemy import select, update



router = APIRouter(prefix="/service", tags=["service"])




@router.post("/", response_model=ServiceSchema)
async def create_service(
        service_creat: ServiceCreat,
        db: AsyncSession = Depends(get_session),
        get_current_bus: UserModel = Depends(get_current_businessman),
):
    inf_ab_buss = await db.scalars(select(BusinessModel).where(BusinessModel.owner_id == get_current_bus.id,
                                                               BusinessModel.is_active == True))

    if not inf_ab_buss.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ваш бизнес не найден")

    db_inf = await db.scalars(select(ServiceModel).where(ServiceModel.business_id == get_current_bus.id,
                                                         ServiceModel.is_active == True))

    if db_inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Такой сервис уже есть")

    model = ServiceModel(**service_creat.model_dump(), business_id=get_current_bus.id)
    db.add(model)
    await db.commit()
    return model


@router.get("/{id_business}", response_model=List[ServiceSchema])
async def get_services(
    id_business: int,
    db: AsyncSession = Depends(get_session),
    current_bus: UserModel = Depends(get_current_businessman),
):
    business = await db.scalar(select(BusinessModel).where(
            BusinessModel.id == id_business,
            BusinessModel.owner_id == current_bus.id,
            BusinessModel.is_active == True)
    )

    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Бизнес не найден или не принадлежит вам")

    services = await db.scalars(select(ServiceModel).where(ServiceModel.business_id == id_business,
                                                           ServiceModel.is_active == True))

    return services.all()