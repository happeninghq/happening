"""Group administration."""

from django.conf.urls import patterns, url


urlpatterns = patterns('plugins.groups.views',
                       url(r'^generate/(?P<pk>\d+)$',
                           'generate_groups',
                           name='generate_groups'),
                       url(r'^(?P<pk>\d+)$',
                           'view_groups',
                           name='view_groups'),
                       url(r'^(?P<pk>\d+)/change_group$',
                           'change_group',
                           name='change_group'),
                       )
