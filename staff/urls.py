"""Member urls."""

from django.conf.urls import url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from staff import views

urlpatterns = [
    url(r'^$', views.index, name='staff'),
    url(r'^members$', views.members, name='staff_members'),
    url(r'^members/(?P<pk>\d+)/staff$', views.make_staff, name='make_staff'),
    url(r'^members/(?P<pk>\d+)/not-staff$', views.make_not_staff,
        name='make_not_staff'),
    url(r'^events$', views.events, name='staff_events'),
    url(r'^event_presets$', views.event_presets, name='event_presets'),
    url(r'^event_presets/create$', views.create_event_preset,
        name='create_event_preset'),
    url(r'^event_presets/(?P<pk>\d+)/edit$', views.edit_event_preset,
        name='edit_event_preset'),
    url(r'^event_presets/(?P<pk>\d+)/delete$', views.delete_event_preset,
        name='delete_event_preset'),
    url(r'^events/create$', views.create_event, name='create_event'),
    url(r'^events/(?P<pk>\d+)$', views.event, name='staff_event'),
    url(r'^events/(?P<pk>\d+)/edit$', views.edit_event, name='edit_event'),
    url(r'^events/(?P<pk>\d+)/email$', views.email_event, name='email_event'),
    url(r'^events/waiting-lists/(?P<pk>\d+)$', views.manage_waiting_list,
        name='manage_waiting_list'),
    url(r'^events/waiting-lists/(?P<pk>\d+)/remove/(?P<user_pk>\d+)$',
        views.remove_from_waiting_list,
        name='remove_from_waiting_list'),
    url(r'^pages$', views.pages, name='staff_pages'),
    url(r'^pages/create$', views.create_page, name='create_page'),
    url(r'^pages/(?P<pk>\d+)$', views.edit_page, name='edit_page'),
    url(r'^pages/(?P<pk>\d+)/delete$', views.delete_page, name='delete_page'),
    url(r'^events/(?P<pk>\d+)/add_attendee$', views.add_attendee,
        name='add_attendee'),
    url(r'^tickets/(?P<pk>\d+)/check_in$', views.check_in, name='check_in'),
    url(r'^tickets/(?P<pk>\d+)/cancel_check_in$', views.cancel_check_in,
        name='cancel_check_in'),
    url(r'^events/(?P<pk>\d+)/manage_check_ins$', views.manage_check_ins,
        name='manage_check_ins'),

    url(r'^emails$', views.staff_emails, name='staff_emails'),
    url(r'^emails/preview$', views.preview_email, name='preview_email'),
    url(r'^emails/(?P<pk>\d+)$', views.email, name='email'),
    url(r'^emails/(?P<pk>\d+)/edit$', views.edit_email, name='edit_email'),
    url(r'^emails/(?P<pk>\d+)/disable$', views.disable_email,
        name='disable_email'),
    url(r'^emails/(?P<pk>\d+)/enable$', views.enable_email,
        name='enable_email'),
    url(r'^emails/(?P<pk>\d+)/delete$', views.delete_email,
        name='delete_email'),
    url(r'^create_email$', views.create_email, name='create_email'),
]

if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p.Plugin, "staff_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                [url(p.Plugin.staff_url_root, include("%s.staff" % plugin))])
