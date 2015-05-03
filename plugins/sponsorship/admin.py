"""Sponsorship administration."""

from django.conf.urls import patterns, url


urlpatterns = patterns('plugins.sponsorship.views',
                       url(r'^sponsorship_tiers$', 'sponsorship_tiers',
                           name='admin_sponsorship_tiers'),
                       url(r'^sponsorship_tiers/create$',
                           'create_sponsorship_tier',
                           name='create_sponsorship_tier'),
                       url(r'^sponsorship_tiers/(?P<pk>\d+)$',
                           'edit_sponsorship_tier',
                           name='edit_sponsorship_tier'),
                       )

admin_links = (
    ("Sponsorship Tiers", "admin_sponsorship_tiers"),
)
