"""Overall URL file."""

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from happening import views
from rest_framework import routers
from happening.api import Api
import os
import inspect
from pages import views as pages_views
from happening.permissions import do_register_permissions
# from ..notifications import api as notifications_api

# Initialise the plugins
from happening.plugins import init

# There isn't a great place to put initialisation code
# so for now we'll put it in the primary urls.py
init()

router = routers.DefaultRouter()

for app in settings.INSTALLED_APPS:
    if os.path.isfile("%s/api.py" % app):
        api = importlib.import_module('%s.api' % app)
        for name, obj in inspect.getmembers(api):
            if inspect.isclass(obj) and issubclass(obj, Api) and\
                    not obj == Api:
                apiname = obj.__name__[:-3].lower()
                router.register(apiname, obj.as_viewset(), base_name=apiname)


urlpatterns = [
    url(r'^$', pages_views.view, {'pk': 'index'}, name='index'),
    url(r'^admin/', include('admin.urls')),
    url(r'^events/', include('events.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^member/', include('members.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^payments/', include('payments.urls')),

    url(r'^upload$', views.file_upload, name='file_upload'),


    url(r'^follow$', views.follow, name='follow'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Load Plugins

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "url_root"):
        # Include the urlpatterns
        urlpatterns += required(
            plugin_enabled_decorator(plugin),
            [url(p.Plugin.url_root, include("%s.urls" % plugin))])

do_register_permissions()
