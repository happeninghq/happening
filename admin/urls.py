"""Admin urls."""

from django.conf.urls import url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from admin import views

urlpatterns = [
    url(r'^$', views.index, name='admin'),
    url(r'^plugins$', views.plugins, name='plugins'),
    url(r'^configuration$', views.configuration, name='configuration'),
]

if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p.Plugin, "admin_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                [url(p.Plugin.admin_url_root, include("%s.admin" % plugin))])
