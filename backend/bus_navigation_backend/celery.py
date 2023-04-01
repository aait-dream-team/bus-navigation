import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'bus_navigation_backend.settings')

app = Celery('bus_navigation_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def hello_world(self):
    print('Hello Celery')

@app.task(bind=True)
def start_serializing(self):
   # Adding import here to avoid apps not loaded yet error.
   from celery_worker.updater import start_serializing
   start_serializing()