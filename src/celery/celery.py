from celery import Celery
from celery.schedules import crontab
from configs.config import settings


celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    include=["tasks.tasks"]
)


celery.conf.beat_schedule = {
    'print-every-5-seconds': {
        'task': 'tasks.tasks.parse_clore',
        'schedule': crontab(minute='*/1')
    },
}
