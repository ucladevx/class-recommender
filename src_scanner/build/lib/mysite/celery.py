from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.task.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'scanner.tasks.add',
#         'schedule': 30.0,
#     },
# }


# from __future__ import absolute_import
# from __future__ import unicode_literals
# import os
# from celery import Celery
# from django.conf import settings
 
# # Indicate Celery to use the default Django settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
 
# app = Celery('mysite')
# app.config_from_object('django.conf:settings')
# # This line will tell Celery to autodiscover all your tasks.py that are in your app folders
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
















