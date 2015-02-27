""" Overall URL file. """

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       # For the time being we will keep the default admin
                       # until all functionality is duplicated
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^staff/', include('staff.urls')),
                       url(r'^events/', include('events.urls')),
                       # Include general external pages as fallback
                       url(r'^', include('external.urls')),

                       (r'^accounts/', include('allauth.urls')),
                       (r'^member/', include('members.urls')),
                       (r'^sponsor/', include('sponsorship.urls')),
                       (r'^notifications/', include('notifications.urls')),

                       # Overriding comments posted redirect
                       (r'^comments/posted/$', 'website.views.comment_posted'),
                       (r'^comments/', include('django_comments.urls')),

                       ) + static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)
