""" Member urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('staff.views',
                       url(r'^$', 'index', name='staff'),
                       url(r'^members$', 'members', name='staff_members'),
                       url(r'^sponsors$', 'sponsors', name='staff_sponsors'),
                       url(r'^events$', 'events', name='staff_events'),
                       url(r'^events/(?P<pk>\d+)$', 'edit_event',
                           name='edit_event'),
                       )
