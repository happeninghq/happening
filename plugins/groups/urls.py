"""Group urls."""

from django.conf.urls import patterns, url

urlpatterns = patterns('plugins.groups.views',
                       url(r'^(?P<pk>\d+)/(?P<group_number>\d+)/edit$',
                           'edit_group', name='edit_group'),
                       )
