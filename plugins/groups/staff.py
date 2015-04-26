"""Group administration."""

from django.conf.urls import patterns, url


urlpatterns = patterns('plugins.groups.views',
                       url(r'^generate/(?P<pk>\d+)$',
                           'generate_groups',
                           name='generate_groups'),
                       )
