"""Event urls."""

from django.conf.urls import url
from events import views
from .feeds import AllEventsFeed

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.view, name='view_event'),
    url(r'^(?P<pk>\d+)/attendees$', views.view_attendees,
        name='view_event_attendees'),
    url(r'^(?P<pk>\d+)/purchase_tickets', views.purchase_tickets,
        name='purchase_tickets'),
    url(r'^tickets_purchased/(?P<pk>\d+)$', views.tickets_purchased,
        name='tickets_purchased'),
    url(r'^(?P<pk>\d+)/wait/leave', views.leave_waiting_list,
        name='leave_waiting_list'),
    url(r'^(?P<pk>\d+)/wait', views.join_waiting_list,
        name='join_waiting_list'),

    url(r'^(?P<pk>\d+)/rsvp/going$', views.rsvp_going, name='rsvp_going'),
    url(r'^(?P<pk>\d+)/rsvp/going/confirm$', views.rsvped_going,
        name='rsvped_going'),
    url(r'^(?P<pk>\d+)/rsvp/not_going$', views.rsvp_not_going,
        name='rsvp_not_going'),

    url(r'^$', views.upcoming_events, name='events'),
    url(r'^past$', views.past_events, name='past_events'),
    url(r'^feeds$', views.feeds, name='event_feeds'),
    url(r'^feeds/all.ics$', AllEventsFeed(), name="all_events_feed"),


    url(r'^(?P<pk>\d+)/payment/$', views.ticket_payment_success,
        name='ticket_payment_success'),
    url(r'^(?P<pk>\d+)/payment/fail$',
        views.ticket_payment_failure,
        name='ticket_payment_failure'),
]
