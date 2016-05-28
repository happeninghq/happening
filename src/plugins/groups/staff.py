"""Group administration."""

from django.conf.urls import url
from plugins.groups import views


urlpatterns = [
    url(r'^generate/(?P<pk>\d+)$', views.generate_groups,
        name='generate_groups'),
    url(r'^(?P<pk>\d+)$', views.view_groups, name='view_groups'),
    url(r'^(?P<pk>\d+)/change_group$', views.change_group,
        name='change_group'),
]
