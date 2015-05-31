"""Sponsorship urls."""

from django.conf.urls import url
from plugins.sponsorship import views

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.view_sponsor, name='view_sponsor'),
]
