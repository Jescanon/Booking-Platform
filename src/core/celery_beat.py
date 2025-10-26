from src.tasks.cheak_booking import event_loop
from celery.schedules import crontab

from src.core.celery_app import celery


celery.conf.beat_schedule = {
    "background-task": {
        "task": "src.tasks.cheak_booking.event_loop",
        "schedule": crontab(minute=59),
        "args": ()
    }

}