"""Event urls."""

from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
                       url(r'^(?P<pk>\d+)$', 'view',
                           name='view_event'),
                       url(r'^(?P<pk>\d+)/purchase_tickets',
                           'purchase_tickets', name='purchase_tickets'),
                       url(r'^tickets_purchased/(?P<pk>\d+)',
                           'tickets_purchased', name='tickets_purchased'),
                       url(r'^$',
                           'events', name='events'),
                       url(r'^(?P<pk>\d+)/vote',
                           'vote', name='vote'),
                       # url(r'^(?P<pk>\d+)/set_group',
                       #     'set_group', name='set_group'),
                       # url(r'^(?P<pk>\d+)/group',
                       #     'group_submission', name='group_submission'),
                       )
