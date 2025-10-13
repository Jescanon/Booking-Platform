from datetime import datetime, timezone

from fastapi import HTTPException, status

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sesiondb import get_session

from src.models.user import User as UserModel

from src.schemas.user import UserCreate, User  as UserSchema

from src.core.security import hashed_password, verify_password

from sqlalchemy import select



router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserSchema)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_session)):
    db_inf = await db.scalars(select(UserModel).where(UserModel.email == user_create.email))
    if db_inf.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такой пользователь уже существет")

    db_config = UserModel(
        email=user_create.email,
        hashed_password=hashed_password(user_create.password),
        role=user_create.role,
        date_joined=datetime.now(timezone.utc),
    )

    db.add(db_config)
    await db.commit()
    return db_config

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_session)):
    db = await db.scalars(select(UserModel).where(UserModel.is_active == True))
    return db.all()