import os
from celery import Celery

# Django sozlamalar modulini Celery uchun o'rnatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Sozlamalarni settings.py dan 'CELERY_' prefiksi bilan o'qish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha ro'yxatdan o'tgan Django ilovalaridan (masalan, quiz/tasks.py) tasklarni avtomatik aniqlash
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Celery Request: {self.request!r}')
