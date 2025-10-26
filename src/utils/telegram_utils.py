from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import update

from src.db.database import session_factory
from src.core.telegram import dp
from src.models.worker import Worker as WorkerModel



def register_handlers(dp):
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        user_id = message.from_user.id

        parts = message.text.split(maxsplit=1)
        link_tg = parts[1] if len(parts) > 1 else None

        if not link_tg:
            await message.answer("Привет! Токен не найден.")
            return

        async with session_factory() as session:
            await session.execute(update(WorkerModel).where(WorkerModel.link_token == link_tg).values(link_token=None,
                                                                                                      telegram_id=user_id))
            await session.commit()

        await message.answer(f"Привет! Твой id: {user_id}")

