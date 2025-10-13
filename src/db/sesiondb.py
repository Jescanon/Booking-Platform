from src.db.database import session_factory
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
