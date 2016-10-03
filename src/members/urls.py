"""Member urls."""

from django.conf.urls import url
from members import views

urlpatterns = [
    url(r'^$', views.index, name='members'),
    url(r'^settings$', views.my_settings, name='my_settings'),
    url(r'^close-account$', views.close_my_account,
        name='close_my_account'),
    url(r'^(?P<pk>\d+)/close-account$', views.close_account,
        name='close_account'),
    url(r'^(?P<pk>\d+)/settings$', views.settings, name='settings'),
    url(r'^(?P<pk>\d+)/settings/username$', views.edit_username,
        name='edit_username'),
    url(r'^(?P<pk>\d+)$', views.view_profile, name='view_profile'),
    url(r'^profile$', views.my_profile, name='my_profile'),
    url(r'^(?P<pk>\d+)/edit$', views.edit_profile, name='edit_profile'),
    url(r'^tickets$', views.my_tickets, name='my_tickets'),
    url(r'^tickets/(?P<pk>\d+)/cancel$', views.cancel_ticket,
        name='cancel_ticket'),
]
