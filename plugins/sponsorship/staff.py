"""Sponsorship administration."""

from django.conf.urls import url
from plugins.sponsorship import views


urlpatterns = [
    url(r'^sponsors$', views.sponsors, name='staff_sponsors'),
    url(r'^sponsors/create$', views.create_sponsor, name='create_sponsor'),
    url(r'^sponsors/(?P<pk>\d+)$', views.staff_view_sponsor,
        name='staff_view_sponsor'),
    url(r'^sponsors/(?P<pk>\d+)/edit$', views.edit_sponsor,
        name='edit_sponsor'),
    url(r'^sponsors/(?P<pk>\d+)/edit/community$',
        views.add_community_sponsorship_to_sponsor,
        name='add_community_sponsorship_to_sponsor'),
    url(r'^sponsors/event/(?P<pk>\d+)$',
        views.add_sponsor_to_event, name='add_sponsor_to_event'),
    url(r'^sponsors/event/(?P<pk>\d+)/remove$',
        views.remove_sponsor_from_event, name='remove_sponsor_from_event'),
]

staff_links = (
    ("Sponsors", "staff_sponsors"),
)
