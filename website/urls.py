""" Overall URL file. """

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^events/', include('events.urls')),
                       # Include general external pages as fallback
                       url(r'^', include('external.urls')),
                       ) + static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)
