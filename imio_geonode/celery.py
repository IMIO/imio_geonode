from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imio_geonode.settings')

from django.conf import settings

app = Celery('imio_geonode',broker='amqp://guest:guest@rabbitmq:5672//')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
#app.config_from_object('django.conf:settings')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
app.conf.update(
	CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler',
)
app.conf.update(
    CELERY_IMPORTS = ["imio_survey.tasks"] 
)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
