""" Event urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
                       url(r'^(?P<pk>\d+)$', 'view',
                           name='view_event'),
                       url(r'^(?P<pk>\d+)/purchase_tickets',
                           'purchase_tickets', name='purchase_tickets'),
                       url(r'^tickets_purchased/(?P<pk>\d+)',
                           'tickets_purchased', name='tickets_purchased'),
                       url(r'^previous',
                           'previous_events', name='previous_events'),
                       )
