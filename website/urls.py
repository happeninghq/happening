""" Overall URL file. """

from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^staff/', include('staff.urls')),
                       url(r'^events/', include('events.urls')),
                       # Include general external pages as fallback
                       url(r'^', include('external.urls')),

                       (r'^accounts/', include('allauth.urls')),
                       (r'^member/', include('members.urls')),
                       (r'^sponsor/', include('sponsorship.urls')),
                       (r'^notifications/', include('notifications.urls')),
                       (r'^pages/', include('pages.urls')),

                       # Overriding comments posted redirect
                       (r'^comments/posted/$', 'website.views.comment_posted'),
                       (r'^comments/', include('django_comments.urls')),

                       ) + static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)
