import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","MemOS.settings")

app = Celery("MemOS")

app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks()