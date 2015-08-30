"""Group urls."""

from django.conf.urls import url
from plugins.groups import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/groups$', views.groups, name='groups'),
    url(r'^(?P<pk>\d+)/groups/(?P<group_number>\d+)$', views.view_group,
        name='view_group'),
    url(r'^(?P<pk>\d+)/groups/(?P<group_number>\d+)/edit$', views.edit_group,
        name='edit_group'),
    url(r'^(?P<pk>\d+)/groups/(?P<group_number>\d+)/join$', views.join_group,
        name='join_group'),
    url(r'^(?P<pk>\d+)/groups/(?P<group_number>\d+)/leave$', views.leave_group,
        name='leave_group'),
    url(r'^(?P<pk>\d+)/groups/add$', views.add_group, name='add_group'),
]
