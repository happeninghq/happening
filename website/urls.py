""" Overall URL file. """

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       # Include general external pages as fallback
                       url(r'^', include('external.urls')),
                       )
