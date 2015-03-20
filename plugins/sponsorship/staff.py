"""Sponsorship administration."""

from django.conf.urls import patterns, url


urlpatterns = patterns('plugins.sponsorship.views',
                       url(r'^sponsors$', 'sponsors', name='staff_sponsors'),
                       url(r'^sponsors/create$', 'create_sponsor',
                           name='create_sponsor'),
                       url(r'^sponsors/(?P<pk>\d+)$', 'staff_view_sponsor',
                           name='staff_view_sponsor'),
                       url(r'^sponsors/(?P<pk>\d+)/edit$', 'edit_sponsor',
                           name='edit_sponsor'),
                       url(r'^sponsors/(?P<pk>\d+)/edit/community$',
                           'add_community_sponsorship_to_sponsor',
                           name='add_community_sponsorship_to_sponsor'),
                       url(r'^sponsors/event/(?P<pk>\d+)$', 'edit_on_event',
                           name='sponsor_edit_on_event'),
                       url(r'^sponsorship_tiers$', 'sponsorship_tiers',
                           name='staff_sponsorship_tiers'),
                       url(r'^sponsorship_tiers/create$',
                           'create_sponsorship_tier',
                           name='create_sponsorship_tier'),
                       url(r'^sponsorship_tiers/(?P<pk>\d+)$',
                           'edit_sponsorship_tier',
                           name='edit_sponsorship_tier'),
                       )

staff_links = (
    ("Sponsors", "staff_sponsors"),
    ("Sponsorship Tiers", "staff_sponsorship_tiers"),
)
