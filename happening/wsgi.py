"""
WSGI config for happening project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling
from os.path import join, dirname, abspath
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "happening.settings")

dotenv_path = join(dirname(abspath(__file__)), '../.env')
load_dotenv(dotenv_path)

application = Cling(MediaCling(get_wsgi_application()))
