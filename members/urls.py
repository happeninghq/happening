""" Member urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('members.views',
                       url(r'^tickets$', 'my_tickets',
                           name='my_tickets'),
                       url(r'^tickets/(?P<pk>\d+)$', 'edit_ticket',
                           name='edit_ticket'),
                       url(r'^tickets/(?P<pk>\d+)/cancel$', 'cancel_ticket',
                           name='cancel_ticket'),
                       )
