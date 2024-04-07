import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_inoa.settings')

app = Celery('desafio_inoa')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()