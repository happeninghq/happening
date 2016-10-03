"""Notification urls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list$', views.list_notifications, name='notifications_list'),
    url(r'^settings$', views.settings, name='notifications_settings'),
    url(r'^unsubscribe$', views.unsubscribe, name='notifications_unsubscribe'),
    url(r'^unsubscribed$', views.unsubscribed,
        name='notifications_unsubscribed'),
    url(r'^all/unsubscribe$', views.unsubscribe_all,
        name='notifications_unsubscribe_all'),
    url(r'^all/unsubscribed$', views.unsubscribed_all,
        name='notifications_unsubscribed_all'),
]
