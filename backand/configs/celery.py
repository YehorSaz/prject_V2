import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('settings')
app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'courses': {
        'task': 'core.services.currencies_service.get_courses',
        'schedule': crontab('0', '8'),
    },
    'update_price': {
        'task': 'core.services.currencies_service.auto_update_price',
        'schedule': crontab('1', '8'),
    }
}
