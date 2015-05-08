"""Group urls."""

from django.conf.urls import patterns, url

urlpatterns = patterns('plugins.groups.views',
                       url(r'^(?P<pk>\d+)/(?P<group_number>\d+)$',
                           'view_group', name='view_group'),
                       url(r'^(?P<pk>\d+)/(?P<group_number>\d+)/edit$',
                           'edit_group', name='edit_group'),
                       url(r'^(?P<pk>\d+)/(?P<group_number>\d+)/join$',
                           'join_group', name='join_group'),
                       url(r'^(?P<pk>\d+)/(?P<group_number>\d+)/leave$',
                           'leave_group', name='leave_group'),
                       url(r'^(?P<pk>\d+)/edit$',
                           'add_group', name='add_group'),
                       )
