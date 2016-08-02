"""Notification urls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list$', views.list_notifications, name='notifications_list'),
    url(r'^settings$', views.settings, name='notifications_settings'),
]
