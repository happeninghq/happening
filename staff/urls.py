"""Member urls."""

from django.conf.urls import patterns, url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required

urlpatterns = patterns('staff.views',
                       url(r'^$', 'index', name='staff'),
                       url(r'^members$', 'members', name='staff_members'),
                       url(r'^members/(?P<pk>\d+)/staff$', 'make_staff',
                           name='make_staff'),
                       url(r'^members/(?P<pk>\d+)/not-staff$',
                           'make_not_staff', name='make_not_staff'),
                       url(r'^send_email$', 'send_email',
                           name='staff_send_email'),
                       url(r'^events$', 'events', name='staff_events'),
                       url(r'^event_presets$', 'event_presets',
                           name='event_presets'),
                       url(r'^event_presets/create$',
                           'create_event_preset', name='create_event_preset'),
                       url(r'^event_presets/(?P<pk>\d+)/edit$',
                           'edit_event_preset', name='edit_event_preset'),
                       url(r'^event_presets/(?P<pk>\d+)/delete$',
                           'delete_event_preset', name='delete_event_preset'),
                       url(r'^events/create$', 'create_event',
                           name='create_event'),
                       url(r'^events/(?P<pk>\d+)$', 'event',
                           name='staff_event'),
                       url(r'^events/(?P<pk>\d+)/edit$', 'edit_event',
                           name='edit_event'),
                       url(r'^events/(?P<pk>\d+)/vote_winner$',
                           'get_vote_winner', name='get_vote_winner'),
                       url(r'^events/(?P<pk>\d+)/email$', 'email_event',
                           name='email_event'),
                       url(r'^pages$', 'pages', name='staff_pages'),
                       url(r'^pages/create$', 'create_page',
                           name='create_page'),
                       url(r'^pages/(?P<pk>\d+)$', 'edit_page',
                           name='edit_page'),
                       url(r'^pages/(?P<pk>\d+)$', 'delete_page',
                           name='delete_page'),
                       url(r'^tickets/(?P<pk>\d+)/check_in$', 'check_in',
                           name='check_in'),
                       url(r'^tickets/(?P<pk>\d+)/cancel_check_in$',
                           'cancel_check_in', name='cancel_check_in'),
                       url(r'^events/(?P<pk>\d+)/manage_check_ins$',
                           'manage_check_ins', name='manage_check_ins'),
                       )

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "staff_url_root"):
        # Include the urlpatterns
        urlpatterns += required(
            plugin_enabled_decorator(plugin),
            patterns(
                '', (p.Plugin.staff_url_root, include("%s.staff" % plugin))))
