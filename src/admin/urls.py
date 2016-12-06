"""Admin urls."""

from django.conf.urls import url, include
from django.conf import settings
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from admin import views


urlpatterns = [
    url(r'^$', views.index, name='admin'),
    url(r'^backup$', views.backup, name='backup'),
    url(r'^backup/(?P<pk>\d+)/cancel$', views.cancel_backup,
        name='cancel_backup'),
    url(r'^backup/(?P<pk>\d+)/delete$', views.delete_backup,
        name='delete_backup'),
    url(r'^backup/schedule$', views.schedule_backup, name='schedule_backup'),
    # url(r'^backup/restore$', views.restore_backup, name='restore_backup'),
    url(r'^plugins$', views.plugins, name='plugins'),
    url(r'^configuration$', views.configuration, name='configuration'),
    url(r'^appearance$', views.appearance, name='appearance'),
    url(r'^menus$', views.menus, name='menus'),
    url(r'^menus/(?P<pk>\d+)/up$', views.move_menu_up,
        name='move_menu_up'),
    url(r'^menus/(?P<pk>\d+)/down$', views.move_menu_down,
        name='move_menu_down'),
    url(r'^menus/(?P<pk>\d+)/delete$', views.delete_menu,
        name='delete_menu'),
    url(r'^payment_handlers$', views.payment_handlers,
        name='payment_handlers'),
    url(r'^payment_handlers/add$', views.add_payment_handler,
        name='add_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/edit$', views.edit_payment_handler,
        name='edit_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/delete$', views.delete_payment_handler,
        name='delete_payment_handler'),
    url(r'^payment_handlers/(?P<pk>\d+)/make_active$',
        views.make_active_payment_handler,
        name='make_active_payment_handler'),

    url(r'^authentication$', views.authentication,
        name='authentication'),
    url(r'^authentication/add$', views.add_authentication,
        name='add_authentication'),
    url(r'^authentication/(?P<pk>\d+)/edit$', views.edit_authentication,
        name='edit_authentication'),
    url(r'^authentication/(?P<pk>\d+)/delete$', views.delete_authentication,
        name='delete_authentication'),
    url(r'^members$', views.members, name='staff_members'),
    url(r'^members/groups$', views.groups, name='groups'),
    url(r'^members/groups/create$', views.create_group, name='create_group'),
    url(r'^members/groups/(?P<pk>\d+)/edit$', views.edit_group, name='edit_group'),
    url(r'^members/export$', views.export_members_to_csv,
        name='export_members_to_csv'),
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
    url(r'^events/(?P<pk>\d+)/export$', views.export_tickets_to_csv,
        name='export_tickets_to_csv'),
    url(r'^events/(?P<pk>\d+)/edit$', views.edit_event, name='edit_event'),
    url(r'^events/(?P<pk>\d+)/email$', views.email_event, name='email_event'),
    url(r'^events/waiting-lists/(?P<pk>\d+)$', views.manage_waiting_list,
        name='manage_waiting_list'),
    url(r'^events/waiting-lists/(?P<pk>\d+)/settings$',
        views.waiting_list_settings,
        name='waiting_list_settings'),
    url(r'^events/waiting-lists/(?P<pk>\d+)/remove/(?P<user_pk>\d+)$',
        views.remove_from_waiting_list,
        name='remove_from_waiting_list'),
    url(r'^events/waiting-lists/(?P<pk>\d+)/release/(?P<user_pk>\d+)$',
        views.release_to_waiting_list,
        name='release_to_waiting_list'),
    url(r'^pages$', views.pages, name='pages'),
    url(r'^pages/create$', views.create_page, name='create_page'),
    url(r'^pages/block$', views.render_block, name='render_block'),
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
    url(r'^tags$', views.tags, name='tags'),
    url(r'^tags/create$', views.create_tag, name='create_tag'),
    url(r'^tags/(?P<pk>\d+)$', views.view_tag, name='view_tag'),
    # url(r'^tags/(?P<pk>\d+)/edit$', views.edit_tag, name='edit_tag'),
    url(r'^tags/(?P<pk>\d+)/delete$', views.delete_tag, name='delete_tag'),
    url(r'^tags/(?P<member_pk>\d+)/(?P<tag_pk>\d+)/remove$', views.remove_tag,
        name='remove_tag'),
    url(r'^tags/(?P<member_pk>\d+)/add$', views.add_tag, name='add_tag'),

    url(r'^tracking-links$', views.tracking_links, name='tracking_links'),
    url(r'^tracking-links/create$', views.create_tracking_link,
        name='create_tracking_link'),
    url(r'^tracking-links/(?P<pk>\d+)/delete$', views.delete_tracking_link,
        name='delete_tracking_link'),
]


if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p.Plugin, "admin_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                [url(p.Plugin.admin_url_root, include("%s.admin" % plugin))])
        if hasattr(p.Plugin, "staff_url_root"):
            # Include the urlpatterns
            urlpatterns += required(
                plugin_enabled_decorator(plugin),
                [url(p.Plugin.staff_url_root, include("%s.staff" % plugin))])
