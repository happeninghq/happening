"""Member urls."""

from django.conf.urls import url
from members import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/settings$', views.settings, name='settings'),
    url(r'^(?P<pk>\d+)/settings/username$', views.edit_username,
        name='edit_username'),
    url(r'^(?P<pk>\d+)$', views.view_profile, name='view_profile'),
    url(r'^(?P<pk>\d+)/edit$', views.edit_profile, name='edit_profile'),
    url(r'^(?P<pk>\d+)/edit/photo$', views.upload_profile_photo,
        name='upload_profile_photo'),
    url(r'^(?P<pk>\d+)/edit/photo/crop$', views.resize_crop_profile_photo,
        name='resize_crop_profile_photo'),
    url(r'^tickets$', views.my_tickets, name='my_tickets'),
    url(r'^tickets/(?P<pk>\d+)$', views.edit_ticket, name='edit_ticket'),
    url(r'^tickets/(?P<pk>\d+)/cancel$', views.cancel_ticket,
        name='cancel_ticket'),
]
