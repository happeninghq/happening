"""Admin views."""
from django.shortcuts import render, redirect, get_object_or_404
from happening.utils import require_permission
from django.conf import settings
import importlib
from django.contrib import messages
from .models import PluginSetting, Backup
from happening.configuration import get_configuration_variables
from happening.configuration import attach_to_form
from happening.configuration import save_variables
from .forms import ConfigurationForm, ThemeForm, SocialAppForm
from payments.models import PaymentHandler
from django.db import transaction
from .forms import PaymentHandlerForm, AddMenuForm
from django.views.decorators.http import require_POST
from django.contrib.sites.models import Site
from django import forms
from allauth.socialaccount.models import SocialApp
from . import tasks
from happening.appearance import THEME_SETTINGS
from collections import OrderedDict
from happening.models import NavigationItemConfiguration
from happening.plugins import navigation_item_name
from happening.plugins import registered_navigation_items, plugin_enabled
from happening.permissions import _registered_permissions, get_permission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from events.models import Event, Ticket, TicketType
from events.forms import EventForm
from pages.models import Page
from .forms import EmailForm, WaitingListForm
from django.utils import timezone
from emails.models import Email
from emails import render_email
from markdown import markdown
from django.http import JsonResponse
from django.utils import formats
from django.views.decorators.csrf import csrf_protect
from djqscsv import render_to_csv_response
from members.forms import TagForm, AddTagForm, TrackingLinkForm
from members.forms import AssignGroupForm
from members.models import Tag, TrackingLink
from django.contrib.auth.models import User
from pages.utils import render_block_content, get_block_types
from admin.forms import PageForm, GroupForm
import json
from members.groups import get_admin_group
from admin.context_processors import admin_urls
from django.urls import reverse, resolve


def can_see_admin(user):
    """Can this user view the admin panel."""
    for url in admin_urls()["admin_urls"]:
        if not url[1] == "admin":
            path = reverse(url[1])
            view = resolve(path).func
            if not hasattr(view, "has_permission") or\
                    view.has_permission(user):
                return True
    return False


@require_permission(func=can_see_admin)
def index(request):
    """Admin dashboard."""
    return render(request, "admin/index.html")


@require_permission("configuration")
def plugins(request):
    """Plugin settings."""
    if request.method == "POST":
        # Save the plugins
        for plugin in settings.PLUGINS:
            preference, _ = PluginSetting.objects.get_or_create(
                plugin_name=plugin)
            preference.enabled = False
            if plugin + "_plugin" in request.POST:
                preference.enabled = True
            preference.save()

        messages.success(request,
                         "Your plugin settings have been saved")
        return redirect("plugins")

    plugins = {}

    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        enabled = False

        preference = PluginSetting.objects.filter(plugin_name=plugin).first()
        if preference:
            enabled = preference.enabled

        plugins[plugin] = {
            "id": plugin,
            "name": p.Plugin.name,
            "description": p.Plugin.__doc__,
            "enabled": enabled}

    return render(request, "admin/configuration/plugins.html",
                  {"plugins": plugins.values()})


@require_permission("configuration")
def configuration(request):
    """Configure settings."""
    variables = get_configuration_variables("configuration")
    form = ConfigurationForm()

    if request.method == "POST":
        form = ConfigurationForm(request.POST)
        attach_to_form(form, variables)
        if form.is_valid():
            save_variables(form, variables)
            messages.success(request, "Configuration updated.")
            return redirect("configuration")
    else:
        attach_to_form(form, variables)

    return render(request, "admin/configuration/index.html",
                  {"form": form})


@require_permission("configuration")
def payment_handlers(request):
    """List payment handlers."""
    payment_handlers = PaymentHandler.objects.all()
    return render(request, "admin/configuration/payment_handlers.html",
                  {"payment_handlers": payment_handlers})


@require_permission("configuration")
def add_payment_handler(request):
    """Add a payment handler."""
    form = PaymentHandlerForm()
    if request.method == "POST":
        form = PaymentHandlerForm(request.POST)
        if form.is_valid():
            payment_handler = form.save()
            if PaymentHandler.objects.all().count() == 1:
                # If it's the only one it has to be active
                payment_handler.active = True
                payment_handler.save()
            messages.success(request, "Payment Handler added.")
            return redirect("payment_handlers")
    return render(request, "admin/configuration/add_payment_handler.html",
                  {"form": form})


@require_permission("configuration")
@require_POST
def delete_payment_handler(request, pk):
    """Delete a payment handler."""
    payment_handler = get_object_or_404(PaymentHandler, pk=pk)
    if payment_handler.active:
        # We need to pass active to another
        next_active = PaymentHandler.objects.exclude(pk=pk).first()
        if next_active:
            next_active.active = True
            next_active.save()
    payment_handler.delete()
    messages.success(request, "Payment Handler deleted.")
    return redirect("payment_handlers")


@require_permission("configuration")
def edit_payment_handler(request, pk):
    """Edit a payment handler."""
    payment_handler = get_object_or_404(PaymentHandler, pk=pk)
    form = PaymentHandlerForm(instance=payment_handler)
    if request.method == "POST":
        form = PaymentHandlerForm(request.POST, instance=payment_handler)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment Handler updated.")
            return redirect("payment_handlers")
    return render(request, "admin/configuration/edit_payment_handler.html",
                  {"form": form, "payment_handler": payment_handler})


@require_permission("configuration")
def make_active_payment_handler(request, pk):
    """Make a payment handler active."""
    with transaction.atomic():
        payment_handler = get_object_or_404(PaymentHandler, pk=pk)
        payment_handler.active = True
        payment_handler.save()

        PaymentHandler.objects.exclude(pk=pk).update(active=False)
    messages.success(request, "Active Payment Handler changed.")
    return redirect("payment_handlers")


@require_permission("appearance")
def appearance(request):
    """Allow configuring logo and css."""
    site = Site.objects.first().happening_site

    initial_data = {"logo": site.logo}

    def setup_form(form):
        for item, value in list(site.get_theme_settings().items()):
            form.fields[item] = forms.CharField(
                widget=forms.TextInput(
                    attrs={'type': 'color'}
                ),
                label=item.replace("-", " ").title())
            form.fields[item].category = value["category"]
            if "tooltip" in value:
                form.fields[item].tooltip = value["tooltip"]
            initial_data[item] = value["value"]

    form = ThemeForm(initial=initial_data)
    setup_form(form)

    if request.method == "POST":
        form = ThemeForm(request.POST)
        setup_form(form)
        if form.is_valid():
            site.theme_settings = {}
            for variable in list(site.get_theme_settings().keys()):
                site.theme_settings[variable] = form.cleaned_data[variable]
            site.logo = form.cleaned_data['logo']
            site.save()

            return redirect("appearance")

    categories = OrderedDict(sorted(THEME_SETTINGS.items()))
    return render(request, "admin/appearance/index.html",
                  {"theme_form": form, "categories": categories})


@require_permission("appearance")
def menus(request):
    """Edit menus."""
    menus = [{"menu": m, "name": navigation_item_name(m.name)}
             for m in NavigationItemConfiguration.objects.all()
             if plugin_enabled(m.name.rsplit(".", 1)[0])]
    allocated_menus = [m["menu"].name for m in menus]

    unallocated_menus = []

    for plugin in registered_navigation_items.keys():
        if plugin_enabled(plugin):
            for k in registered_navigation_items[plugin].keys():
                plugin_key = "%s.%s" % (plugin, k)
                if plugin_key not in allocated_menus:
                    unallocated_menus.append((plugin_key,
                                             registered_navigation_items[
                                                 plugin][k]["name"]))

    form = None
    if len(unallocated_menus) > 0:
        form = AddMenuForm(menus=unallocated_menus)
        if request.method == "POST":
            form = AddMenuForm(request.POST, menus=unallocated_menus)
            if form.is_valid():
                form.save()
                return redirect("menus")

    return render(request, "admin/appearance/menus.html",
                  {"menus": menus, "form": form})


@require_permission("appearance")
def move_menu_up(request, pk):
    """Move menu up."""
    NavigationItemConfiguration.objects.get(pk=pk).up()
    return redirect("menus")


@require_permission("appearance")
def move_menu_down(request, pk):
    """Move menu down."""
    NavigationItemConfiguration.objects.get(pk=pk).down()
    return redirect("menus")


@require_permission("appearance")
def delete_menu(request, pk):
    """Delete menu."""
    NavigationItemConfiguration.objects.get(pk=pk).delete()
    return redirect("menus")


@require_permission("configuration")
def authentication(request):
    """List social apps."""
    social_apps = SocialApp.objects.all()
    return render(request, "admin/configuration/authentication.html",
                  {"social_apps": social_apps})


@require_permission("configuration")
def add_authentication(request):
    """Add a social app."""
    form = SocialAppForm()
    if request.method == "POST":
        form = SocialAppForm(request.POST)
        if form.is_valid():
            social_app = form.save()
            social_app.sites.add(Site.objects.first())
            messages.success(request, "Authentication provider added.")
            return redirect("authentication")
    return render(request, "admin/configuration/add_authentication.html",
                  {"form": form})


@require_permission("configuration")
@require_POST
def delete_authentication(request, pk):
    """Delete a social app."""
    social_app = get_object_or_404(SocialApp, pk=pk)
    social_app.delete()
    messages.success(request, "Authentication provider deleted.")
    return redirect("authentication")


@require_permission("configuration")
def edit_authentication(request, pk):
    """Edit a social app."""
    social_app = get_object_or_404(SocialApp, pk=pk)
    form = SocialAppForm(instance=social_app)
    if request.method == "POST":
        form = SocialAppForm(request.POST, instance=social_app)
        if form.is_valid():
            form.save()
            messages.success(request, "Authentication provider updated.")
            return redirect("authentication")
    return render(request, "admin/configuration/edit_authentication.html",
                  {"form": form, "social_app": social_app})


@require_permission("backup")
def backup(request):
    """Allow dumping/restoring data."""
    return render(
        request,
        "admin/backup.html",
        {"backups": Backup.objects.filter(restore=False),
         "backup_scheduled": Backup.objects.filter(
            restore=False, complete=False).count() > 0,
         "restore_scheduled": Backup.objects.filter(
            restore=True).count() > 0})


@require_permission("backup")
@require_POST
def schedule_backup(request):
    """Dump zip of data and media."""
    tasks.backup.delay()
    messages.success(request, "Backup has been scheduled. It will be " +
                     "complete within 20 minutes.")
    return redirect("backup")


# @require_permission("backup")
# @require_POST
# def restore_backup(request):
#     """Restore zip to database."""
#     backup = Backup(zip_file=request.FILES['zip_file'], restore=True)
#     backup.save()
#     tasks.restore.delay(backup.pk)
#     messages.success(request, "Restore has been scheduled. It will be " +
#                      "complete within 20 minutes.")
#     return redirect("backup")


@require_permission("backup")
@require_POST
def delete_backup(request, pk):
    """Delete a backup."""
    backup = get_object_or_404(Backup, pk=pk)
    if not backup.complete:
        messages.error(request, "That backup has not yet completed.")
        return redirect("backup")
    backup.delete()
    messages.success(request, "Backup has been deleted.")
    return redirect("backup")


@require_permission("backup")
@require_POST
def cancel_backup(request, pk):
    """Cancel a backup."""
    backup = get_object_or_404(Backup, pk=pk)
    if backup.started:
        messages.error(request, "That backup has started.")
        return redirect("backup")
    backup.delete()
    messages.success(request, "Backup has been cancelled.")
    return redirect("backup")


@require_permission("manage_members")
def members(request):
    """Administrate members."""
    members = get_user_model().objects.all()
    return render(request, "admin/members/index.html", {"members": members})


@require_permission("manage_members", "manage_groups")
def groups(request):
    """Administrate groups."""
    groups = Group.objects.all()
    return render(request, "admin/members/groups.html", {"groups": groups})


@require_permission("manage_members", "manage_groups")
def create_group(request):
    """Create groups."""
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created.")
            return redirect("groups")
    return render(request, "admin/members/create_group.html", {"form": form})


def _build_permission_groups(group):
    """Build permission groups for use in edit_group."""
    permissions = {}
    for g in _registered_permissions.keys():
        if g not in permissions:
            permissions[g] = {}
        for key in _registered_permissions[g].keys():
            permission = _registered_permissions[g][key]
            permission_object = get_permission(g, key)
            permissions[g][key] = {
                "pk": permission_object.pk,
                "name": permission["name"],
                "description": permission["description"],
                "enabled": group.permissions.filter(
                    pk=permission_object.pk).count() > 0,
                "object": permission_object
            }
    return permissions


@require_permission("manage_members", "manage_groups")
def edit_group(request, pk):
    """Edit a group."""
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=group)

    allow_modify_permissions = True
    if group == get_admin_group():
        allow_modify_permissions = False

    # Create the set of permissions
    permissions = _build_permission_groups(group)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()

            # Now save permissions
            for p in permissions:
                for key, d in permissions[p].items():
                    permission_object = d["object"]
                    if ("permission_" + str(permission_object.pk)
                            in request.POST):
                        # Should be enabled
                        if not d["enabled"]:
                            # Need to enable it
                            group.permissions.add(permission_object)
                    else:
                        # Should not be enabled
                        if d["enabled"]:
                            # Need to disable it
                            group.permissions.remove(permission_object)

                group.save()

            messages.success(request, "Group updated.")
            return redirect("groups")
    return render(request, "admin/members/edit_group.html",
                  {"group": group, "form": form, "permissions": permissions,
                   "allow_modify_permissions": allow_modify_permissions})


@require_permission("manage_members", "manage_groups")
@require_POST
def assign_to_group(request, member_pk):
    """Assign a member to a group."""
    member = get_object_or_404(get_user_model(), pk=member_pk)
    form = AssignGroupForm(request.POST, member=member)
    if form.is_valid():
        group = get_object_or_404(Group, pk=form.cleaned_data['group'])
        member.groups.add(group)
        messages.success(request, "The member has been assigned to the group.")
    return redirect("view_profile", member.pk)


@require_permission("manage_members", "manage_groups")
def remove_from_group(request, member_pk, group_pk):
    """Remove a member from a group."""
    member = get_object_or_404(get_user_model(), pk=member_pk)
    group = get_object_or_404(Group, pk=group_pk)
    member.groups.remove(group)
    messages.success(request, "The member has been removed from the group.")
    return redirect("view_profile", member.pk)


@require_permission("manage_members")
def export_members_to_csv(request):
    """Export members to CSV."""
    members = get_user_model().objects.all().values("username", "email")
    return render_to_csv_response(members)


@require_permission("manage_events")
def events(request):
    """Administrate events."""
    events = Event.objects.all().order_by('-start')
    return render(request, "admin/events.html", {"events": events})


@require_permission("manage_events")
def export_tickets_to_csv(request, pk):
    """Export tickets to csv."""
    event = get_object_or_404(Event, pk=pk)
    tickets = event.tickets.all().values("user__username", "user__email",
                                         "cancelled", "type__name",
                                         "checked_in", "checked_in_datetime")
    return render_to_csv_response(tickets)


@require_permission("manage_events")
def add_attendee(request, pk):
    """Add an attendee to the event.

    This is available after the event has started and will mark
    the ticket as being added late.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        user = get_object_or_404(
            get_user_model(), pk=request.POST['member_pk'])
        ticket, created = Ticket.objects.get_or_create(event=event, user=user,
                                                       cancelled=False)
        messages.success(request, "%s added to event." % user.profile)
        return redirect("staff_event", event.pk)

    members = get_user_model().objects.all()

    members = [m for m in members if not
               m.tickets.filter(event=event, cancelled=False).count() > 0]

    return render(request, "admin/add_attendee.html",
                  {"event": event,
                   "members": members})


@require_permission("manage_events")
def check_in(request, pk):
    """Check in a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if not ticket.checked_in:
        ticket.checked_in = True
        ticket.checked_in_datetime = timezone.now()
        ticket.save()
        if not request.is_ajax():
            messages.success(request, ticket.user.name() +
                             " has been checked in.")
    if request.is_ajax():
        return JsonResponse({"checked-in": "True<br /> " +
                            formats.date_format(
                                ticket.checked_in_datetime,
                                "DATETIME_FORMAT")})
    return redirect(request.GET.get("next"))


@require_permission("manage_events")
def cancel_check_in(request, pk):
    """Cancel the check in for a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.checked_in:
        ticket.checked_in = False
        ticket.checked_in_datetime = timezone.now()
        ticket.save()
        if not request.is_ajax():
            messages.success(request, ticket.user.name() +
                             " is no longer checked in.")

    if request.is_ajax():
        return JsonResponse({"checked-in": "False"})
    return redirect(request.GET.get("next"))


@require_permission("manage_events")
def manage_check_ins(request, pk):
    """Manage check ins."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "admin/manage_check_ins.html", {"event": event})


@require_permission("manage_events")
def event(request, pk):
    """View event."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "admin/event.html", {"event": event})


@require_permission("manage_events")
def edit_event(request, pk):
    """Edit event."""
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    variables = get_configuration_variables("event_configuration", event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        attach_to_form(form, variables, editing=True)
        if form.is_valid():
            form.save()
            save_variables(form, variables)
            return redirect("staff_event", event.pk)
    else:
        attach_to_form(form, variables, editing=True)
    return render(request, "admin/edit_event.html",
                  {"event": event, "form": form})


@require_permission("manage_events")
def create_event(request):
    """Create event."""
    form = EventForm()
    variables = get_configuration_variables("event_configuration")
    if request.method == "POST":
        form = EventForm(request.POST)
        attach_to_form(form, variables)
        if form.is_valid():
            event = form.save()
            variables = get_configuration_variables("event_configuration",
                                                    event)
            save_variables(form, variables)

            return redirect("staff_events")
    else:
        attach_to_form(form, variables)
    return render(request, "admin/create_event.html",
                  {"form": form})


# We had to add csrf_protect below because of django not generating a token
# TODO: Figure out why this is an remove it. It should be automatic
@require_permission("manage_events")
@csrf_protect
def manage_waiting_list(request, pk):
    """Manage waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    form = WaitingListForm(initial={"automatic":
                                    ticket_type.waiting_list_automatic})
    return render(request, "admin/manage_waiting_list.html",
                  {"ticket_type": ticket_type, "form": form})


@require_permission("manage_events")
@require_POST
def waiting_list_settings(request, pk):
    """Manage waiting list settings."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    form = WaitingListForm(request.POST)
    if form.is_valid():
        ticket_type.waiting_list_automatic =\
            form.cleaned_data['automatic']
        ticket_type.save()
        return redirect("manage_waiting_list", pk)


@require_permission("manage_events")
def remove_from_waiting_list(request, pk, user_pk):
    """Remove a user from a waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)
    ticket_type.leave_waiting_list(user)

    messages.success(request,
                     "%s has been removed from the waiting list." % user)

    return redirect("manage_waiting_list", pk)


@require_permission("manage_events")
def release_to_waiting_list(request, pk, user_pk):
    """Release a ticket to a user on the waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    waiting_list = user.waiting_lists.filter(ticket_type=ticket_type).first()

    if not waiting_list:
        return redirect("manage_waiting_list", pk)

    waiting_list.set_can_purchase()
    waiting_list.save()

    messages.success(request,
                     "%s can now purchase tickets." % user)

    return redirect("manage_waiting_list", pk)


@require_permission("manage_emails")
def preview_email(request):
    """Render an email as it would be sent."""
    if request.GET.get('event'):
        event = get_object_or_404(Event, pk=request.GET['event'])
    else:
        event = None

    subject = render_email(request.GET['subject'], request.user, event)
    content = render_email(request.GET['content'], request.user, event)

    # Then apply markdown
    content = markdown(content)

    return JsonResponse({"subject": subject, "content": content})


@require_permission("manage_emails")
def email_event(request, pk):
    """Send an email to attendees."""
    event = get_object_or_404(Event, pk=pk)
    form = EmailForm(initial={
        "to": "tickets__has:(event__id:%s cancelled:False)" % event.id,
        "subject": event.title
    })
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.event = event
            instance.save()
            messages.success(request, "Email created")
            return redirect("staff_emails")
    return render(request, "admin/email_event.html",
                  {"event": event, "form": form})


@require_permission("appearance")
def pages(request):
    """Administrate pages."""
    pages = Page.objects.all()
    return render(request, "admin/appearance/pages.html", {"pages": pages})


@require_permission("appearance")
def render_block(request):
    """Used to render block previews on the page editor."""
    return JsonResponse({"html": render_block_content(request.GET, request)})


@require_permission("appearance")
def edit_page(request, pk):
    """Edit page."""
    page = get_object_or_404(Page, pk=pk)

    if request.method == "POST":
        # TODO: Validate the posted data
        page.content = json.loads(request.POST['content'])
        page.save()
        messages.success(request, 'Page saved.')
        return redirect("pages")

    return render(request, "admin/appearance/edit_page.html",
                  {"page": page, "block_types": get_block_types()})


@require_permission("appearance")
def delete_page(request, pk):
    """Delete page."""
    page = get_object_or_404(Page, pk=pk)
    page.delete()
    return redirect("pages")


@require_permission("appearance")
def create_page(request):
    """Create page."""
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = Page(url=form.cleaned_data['url'],
                        title=form.cleaned_data['title'])
            page.save()
            messages.success(request, 'Page created.')
            return redirect("pages")
    return render(request, "admin/appearance/create_page.html", {"form": form})


@require_permission("manage_emails")
def staff_emails(request):
    """List emails."""
    return render(request,
                  "admin/emails.html",
                  {"emails": Email.objects.all()})


@require_permission("manage_emails")
def email(request, pk):
    """Show email details."""
    email = get_object_or_404(Email, pk=pk)
    return render(request,
                  "admin/email.html",
                  {"email": email})


@require_permission("manage_emails")
def create_email(request):
    """Send an email."""
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Email created")
            return redirect("staff_emails")
    return render(request, "admin/create_email.html",
                  {"form": form})


@require_permission("manage_emails")
def edit_email(request, pk):
    """Edit an email."""
    email = get_object_or_404(Email, pk=pk)
    form = EmailForm(instance=email)
    if request.method == "POST":
        form = EmailForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            messages.success(request, "Email edited")
            return redirect(request.GET.get("redirect", "staff_emails"))
    return render(request, "admin/edit_email.html",
                  {"form": form, "email": email})


@require_permission("manage_emails")
def disable_email(request, pk):
    """Disable an email."""
    email = get_object_or_404(Email, pk=pk)
    email.disabled = True
    email.save()
    messages.success(request, "The email has been disabled")
    return redirect(request.GET.get("redirect", "staff_emails"))


@require_permission("manage_emails")
def enable_email(request, pk):
    """Enable an email."""
    email = get_object_or_404(Email, pk=pk)
    email.disabled = False
    email.save()
    messages.success(request, "The email has been enabled")
    return redirect(request.GET.get("redirect", "staff_emails"))


@require_permission("manage_emails")
@require_POST
def delete_email(request, pk):
    """Delete an email."""
    email = get_object_or_404(Email, pk=pk)
    if email.sent_emails.count() > 0:
        messages.error(request, "You can not delete an email which has been " +
                       "sent. Disable it instead.")
    else:
        email.delete()
        messages.success(request, "The email has been deleted")
    return redirect(request.GET.get("redirect", "staff_emails"))


@require_permission("manage_members")
def tags(request):
    """List tags."""
    tags = Tag.objects.all()
    return render(request, "admin/members/tags.html",
                  {"tags": tags})


@require_permission("manage_members")
def create_tag(request):
    """Add a tag."""
    form = TagForm()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The tag has been created.")
            return redirect("tags")
    return render(request, "admin/members/create_tag.html", {"form": form})


@require_permission("manage_members")
@require_POST
def delete_tag(request, pk):
    """Delete a tag."""
    tag = get_object_or_404(Tag, pk=pk)
    if tag.users.count() > 0:
        messages.error(request, "The tag cannot be deleted as it is in use")
        return redirect("tags")
    tag.delete()
    messages.success(request, "The tag has been deleted.")
    return redirect("tags")


@require_permission("manage_members")
def view_tag(request, pk):
    """View a promocode."""
    tag = get_object_or_404(Tag, pk=pk)
    return render(request, "admin/members/view_tag.html", {"tag": tag})


@require_permission("manage_members")
@require_POST
def add_tag(request, member_pk):
    """Add a tag."""
    member = get_object_or_404(User, pk=member_pk)
    form = AddTagForm(request.POST, member=member)
    form = AddTagForm(request.POST, member=member)
    if form.is_valid():
        member.tags.add(form.cleaned_data['tag'])
        messages.success(request, "The tag has been added.")
    return redirect("view_profile", member_pk)


@require_permission("manage_members")
@require_POST
def remove_tag(request, member_pk, tag_pk):
    """Remove a tag."""
    member = get_object_or_404(User, pk=member_pk)
    tag = get_object_or_404(Tag, pk=tag_pk)
    member.tags.remove(tag)
    messages.success(request, "The tag has been removed.")
    return redirect("view_profile", member_pk)


@require_permission("manage_members")
def tracking_links(request):
    """List tracking links."""
    tracking_links = TrackingLink.objects.all()
    return render(request, "admin/members/tracking_links.html",
                  {"tracking_links": tracking_links})


@require_permission("manage_members")
def create_tracking_link(request):
    """Add a tracking link."""
    form = TrackingLinkForm()
    if request.method == "POST":
        form = TrackingLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The tracking link has been created.")
            return redirect("tracking_links")
    return render(request, "admin/members/create_tracking_link.html",
                  {"form": form})


@require_permission("manage_members")
@require_POST
def delete_tracking_link(request, pk):
    """Delete a tracking link."""
    tracking_link = get_object_or_404(TrackingLink, pk=pk)
    tracking_link.delete()
    messages.success(request, "The tracking link has been deleted.")
    return redirect("tracking_links")
