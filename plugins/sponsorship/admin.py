"""Sponsorship administration."""

from django.conf.urls import url
from plugins.sponsorship import views


urlpatterns = [
    url(r'^sponsorship_tiers$', views.sponsorship_tiers,
        name='admin_sponsorship_tiers'),
    url(r'^sponsorship_tiers/create$', views.create_sponsorship_tier,
        name='create_sponsorship_tier'),
    url(r'^sponsorship_tiers/(?P<pk>\d+)$', views.edit_sponsorship_tier,
        name='edit_sponsorship_tier'),
]

admin_links = (
    ("Sponsorship Tiers", "admin_sponsorship_tiers"),
)
