"""Notification urls."""

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^list$', views.list, name='notifications_list'),
    url(r'^mark-read$', views.mark_read, name='notifications_mark_read'),
    url(r'^settings$', views.settings, name='notifications_settings'),
]
