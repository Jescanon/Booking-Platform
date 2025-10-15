import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.config import SECRET_KEY, ALGORITHM
from src.db.sesiondb import get_session
from src.models.user import User as UserModel, User

from datetime import datetime, timedelta, timezone

out2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TIME_INFO_IN_ACCESS_TOKEN = 40

def hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    datas = data.copy()
    exp_info = datetime.now(timezone.utc) + timedelta(minutes=TIME_INFO_IN_ACCESS_TOKEN)
    datas.update({"exp": exp_info})
    return jwt.encode(datas, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(out2_scheme), db: AsyncSession = Depends(get_session)):
    code_eror = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise code_eror

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.PyJWTError:
        raise code_eror

    user = await db.scalars(select(UserModel).where(UserModel.email == email ,UserModel.is_active == True))
    users = user.first()

    if not users:
        raise code_eror

    return users

async def get_current_businessman(current_user: User = Depends(get_current_user)):
    if current_user.role != "businessman":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только бизнесмены могут это редактировать")

    return current_user

