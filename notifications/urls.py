"""Notification urls."""

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^list$', views.list, name='notifications_list'),
    url(r'^settings$', views.settings, name='notifications_settings'),
]
