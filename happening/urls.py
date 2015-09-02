"""Overall URL file."""

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from happening import views

urlpatterns = [
    url(r'^staff/', include('staff.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^events/', include('events.urls')),

    # Include general external pages as fallback
    url(r'^', include('external.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^member/', include('members.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^payments/', include('payments.urls')),

    url(r'^upload$', views.file_upload, name='file_upload'),


    url(r'^follow$', views.follow, name='follow'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "url_root"):
        # Include the urlpatterns
        urlpatterns += required(
            plugin_enabled_decorator(plugin),
            [url(p.Plugin.url_root, include("%s.urls" % plugin))])
