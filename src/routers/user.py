from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status, APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sesiondb import get_session

from src.models.user import User as UserModel

from src.schemas.user import UserCreate, User  as UserSchema

from src.core.security import hashed_password, verify_password, create_access_token, get_current_user

from sqlalchemy import select, update


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserSchema)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_session)):
    db_inf = await db.scalars(select(UserModel).where(UserModel.email == user_create.email))
    if db_inf.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Такой пользователь уже существет")

    db_config = UserModel(email=user_create.email,
                          hashed_password=hashed_password(user_create.password),
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

    access_token = create_access_token({"sub": users.email,
                                        "role": users.role,
                                        "id": users.id,
                                        "created_at": str(users.date_joined)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/info-user", response_model=UserSchema)
async def read_users_me(user: UserSchema = Depends(get_current_user)):
    return user


@router.put("/update/{user_id}", response_model=UserSchema)
async def update_user(user_id: int,
                      new_user: UserCreate,
                      user: UserModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session),
                      ):
    inf_in_usr = await db.scalars(select(UserModel).where(UserModel.is_active == True,
                                                          UserModel.id == user_id))
    inf = inf_in_usr.first()
    if not inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Юзер не найден")
    if inf.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="вы не можете менять данного юзера")

    inos = await db.scalars(select(UserModel).where(UserModel.email ==  user.email,
                                                    UserModel.is_active == True))
    sec = inos.first()

    if sec and sec.email != new_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с такой почтой уже есть")


    await db.execute(update(UserModel).where(UserModel.id == user_id).values(email=new_user.email,
                                                                             hashed_password=hashed_password(new_user.password)))
    await db.commit()
    await db.refresh(inf)
    return inf

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int,
                      db: AsyncSession = Depends(get_session),
                      user: UserModel = Depends(get_current_user)):

    inf_in_usr = await db.scalars(select(UserModel).where(UserModel.is_active == True,
                                                          UserModel.id == user_id))
    inf = inf_in_usr.first()
    if not inf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Юзер не найден")
    if user.role != "admin":
        if inf.id != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="У вас нету прав удалить данного пользователя")

    await db.execute(update(UserModel).where(UserModel.id == user_id).values(is_active=False))
    await db.commit()
    return {"success": "Пользователь удален"}



