from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kucoinapi.settings')

app = Celery('kucoinapi')
app.conf.enable_utc = False

app.conf.update(timezone='UTC')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'fetch_exchange_data':{
        'task': 'tread.tasks.send_notifiction',
        'schedule': 20,
}
}

app.autodiscover_tasks()

