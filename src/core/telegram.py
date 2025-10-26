import asyncio
from aiogram import Bot, Dispatcher
from src.core.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("Бот запускается")

    from src.utils.telegram_utils import register_handlers
    register_handlers(dp)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"Ошибка {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
