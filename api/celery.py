import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-countries-every-hour': {
        'task': 'country.tasks.fetch_countries_data',
        'schedule': crontab(minute='0',hour='*'),
    },
}