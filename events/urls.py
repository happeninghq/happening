""" Event urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
                       url(r'^(?P<pk>.+)$', 'view',
                           name='view_event'),
                       )
