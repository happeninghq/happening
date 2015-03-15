""" Member urls. """

from django.conf.urls import patterns, url, include
from django.conf import settings
import importlib

urlpatterns = patterns('admin.views',
                       url(r'^$', 'index', name='admin'),
                       url(r'^plugins$', 'plugins', name='plugins'),
                       )

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "admin_url_root"):
        # Include the urlpatterns
        urlpatterns += patterns(
            '', (p.Plugin.admin_url_root, include("%s.admin" % plugin)))
