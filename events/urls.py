"""Event urls."""

from django.conf.urls import url
from events import views

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.view, name='view_event'),
    url(r'^(?P<pk>\d+)/purchase_tickets', views.purchase_tickets,
        name='purchase_tickets'),
    url(r'^tickets_purchased/(?P<pk>\d+)', views.tickets_purchased,
        name='tickets_purchased'),
    url(r'^$', views.events, name='events'),
    url(r'^(?P<pk>\d+)/vote', views.vote, name='vote'),
]
