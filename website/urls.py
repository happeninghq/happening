""" Overall URL file. """

from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
import importlib

urlpatterns = patterns('',
                       url(r'^staff/', include('staff.urls')),
                       url(r'^events/', include('events.urls')),
                       # Include general external pages as fallback
                       url(r'^', include('external.urls')),

                       (r'^accounts/', include('allauth.urls')),
                       (r'^member/', include('members.urls')),
                       (r'^notifications/', include('notifications.urls')),
                       (r'^pages/', include('pages.urls')),

                       # Overriding comments posted redirect
                       (r'^comments/posted/$', 'website.views.comment_posted'),
                       (r'^comments/', include('django_comments.urls')),

                       ) + static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "url_root"):
        # Include the urlpatterns
        urlpatterns += patterns(
            '', (p.Plugin.url_root, include("%s.urls" % plugin)))
