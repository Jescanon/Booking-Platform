from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sesiondb import get_session

from src.models.user import User as UserModel

from src.schemas.user import UserCreate, User  as UserSchema

from src.core.security import hashed_password, verify_password, create_access_token, get_current_user

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

@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    db = await db.scalars(select(UserModel).where(UserModel.is_active == True))
    return db.all()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  db: AsyncSession = Depends(get_session)):
    user = await db.scalars(select(UserModel).where(UserModel.email == form_data.username,
                                                    UserModel.is_active == True))
    users = user.first()

    if not users or not verify_password(form_data.password, users.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token({"sub": users.email, "role": users.role, "id": users.id, "created_at": str(users.date_joined)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/info-user", response_model=UserSchema)
async def read_users_me(user: UserSchema = Depends(get_current_user)):
    return user