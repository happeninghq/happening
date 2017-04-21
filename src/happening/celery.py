from __future__ import absolute_import

import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv
import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
from django.conf import settings


dotenv_path = join(dirname(abspath(__file__)), '../.env')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'happening.settings')

from django.conf import settings  # noqa


class Celery(celery.Celery):
    """Override so we can log to sentry."""

    def on_configure(self):
        """Override so we can log to sentry."""
        if settings.SENTRY_DSN:
            client = raven.Client(settings.SENTRY_DSN)

            # register a custom filter to filter out duplicate logs
            register_logger_signal(client)

            # hook into the Celery error handler
            register_signal(client)


app = Celery('happening')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
