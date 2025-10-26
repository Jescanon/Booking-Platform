from src.core.celery_app import celery
import asyncio
from src.core.telegram import bot



@celery.task(name="src.tasks.send_message_tg")
def send_message_tg(data):
    async def message_tg(data):
        msg = (f"Привет {data['worker_name']}\n"
               f"У тебя запись на {data['start_time']}\n"
               f"Записавшийся человек {data['user_id']}")
        await bot.send_message(chat_id=data['worker_telegram_id'], text=msg)
    asyncio.run(message_tg(data))
