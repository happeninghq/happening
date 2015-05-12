"""Member urls."""

from django.conf.urls import patterns, url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required

urlpatterns = patterns('admin.views',
                       url(r'^$', 'index', name='admin'),
                       url(r'^plugins$', 'plugins', name='plugins'),
                       url(r'^configuration$', 'configuration',
                           name='configuration'),
                       )

if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p.Plugin, "admin_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                patterns(
                    '', (p.Plugin.admin_url_root,
                         include("%s.admin" % plugin))))
