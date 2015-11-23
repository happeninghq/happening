"""Admin urls."""

from django.conf.urls import url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from admin import views

urlpatterns = [
    url(r'^$', views.index, name='admin'),
    url(r'^backup$', views.backup, name='backup'),
    url(r'^backup/(?P<pk>\d+)/cancel$', views.cancel_backup,
        name='cancel_backup'),
    url(r'^backup/(?P<pk>\d+)/delete$', views.delete_backup,
        name='delete_backup'),
    url(r'^backup/schedule$', views.schedule_backup, name='schedule_backup'),
    url(r'^backup/restore$', views.restore_backup, name='restore_backup'),
    url(r'^plugins$', views.plugins, name='plugins'),
    url(r'^configuration$', views.configuration, name='configuration'),
    url(r'^appearance$', views.appearance, name='appearance'),
    url(r'^appearance/css$', views.generate_css, name='generate_css'),
    url(r'^payment_handlers$', views.payment_handlers,
        name='payment_handlers'),
    url(r'^payment_handlers/add$', views.add_payment_handler,
        name='add_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/edit$', views.edit_payment_handler,
        name='edit_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/delete$', views.delete_payment_handler,
        name='delete_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/make_active$',
        views.make_active_payment_handler,
        name='make_active_payment_handler'),

    url(r'^authentication$', views.authentication,
        name='authentication'),
    url(r'^authentication/add$', views.add_authentication,
        name='add_authentication'),
    url(r'^authentication/(?P<pk>\d+)/edit$', views.edit_authentication,
        name='edit_authentication'),
    url(r'^authentication/(?P<pk>\d+)/delete$', views.delete_authentication,
        name='delete_authentication'),
]

if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p.Plugin, "admin_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                [url(p.Plugin.admin_url_root, include("%s.admin" % plugin))])
