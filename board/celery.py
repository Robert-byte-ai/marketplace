import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')

app = Celery('board')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'ads_messages': {
        'task': 'main.tasks.ads_message',
        'schedule': crontab(
            day_of_week='monday',
            hour=17
        )
    }
}

app.conf.timezone = 'UTC'
