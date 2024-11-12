from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_backend.settings')

app = Celery('gestion_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()