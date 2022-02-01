import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_mailing_for_subscribers': {
        'task': 'src.users.tasks.send_selection',
        'schedule': crontab(day_of_week='sunday'),
    },
}