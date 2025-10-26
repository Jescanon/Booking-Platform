from fastapi import APIRouter
from celery import Celery

router = APIRouter(tags=["Celery"], prefix="/api")

celery = Celery(
    __name__,
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True,
    include=['src.tasks.send_message_tg']
)
