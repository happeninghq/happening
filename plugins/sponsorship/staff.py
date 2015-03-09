""" Sponsorship administration. """

from django.conf.urls import patterns, url


urlpatterns = patterns('plugins.sponsorship.views',
                       url(r'^sponsors$', 'sponsors', name='staff_sponsors'),
                       url(r'^sponsors/create$', 'create_sponsor',
                           name='create_sponsor'),
                       url(r'^sponsors/(?P<pk>\d+)$', 'edit_sponsor',
                           name='edit_sponsor'),
                       url(r'^sponsors/event/(?P<pk>\d+)$', 'edit_on_event',
                           name='sponsor_edit_on_event'),
                       )

staff_links = (
    ("Sponsors", "staff_sponsors"),
)
