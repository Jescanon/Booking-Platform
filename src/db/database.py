from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.core.config import configs


async_engine = create_async_engine(configs.get_engine_db(), echo=True)

session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass