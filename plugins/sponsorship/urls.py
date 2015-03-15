"""Sponsorship urls."""

from django.conf.urls import patterns, url

urlpatterns = patterns('plugins.sponsorship.views',
                       url(r'^(?P<pk>\d+)$', 'view_sponsor',
                           name='view_sponsor'),
                       )
