"""Socal Links administration."""

from django.conf.urls import url
from plugins.social_links import views


urlpatterns = [
    url(r'^$', views.social_links, name='social_links'),
    url(r'^create$', views.create_social_link, name='create_social_link'),
    url(r'^(?P<pk>\d+)/edit$', views.edit_social_link,
        name='edit_social_link'),
    url(r'^(?P<pk>\d+)/delete$', views.delete_social_link,
        name='delete_social_link'),
]

admin_links = (
    ("Social Links", "social_links"),
)
