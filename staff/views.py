"""Staff views."""
from happening.utils import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from events.models import Event, Ticket, EventPreset
from events.forms import EventForm
from pages.models import Page
from pages.forms import PageForm
from forms import EmailForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from admin.notifications import AdminEventMessageNotification
from admin.notifications import AdminMessageNotification
from django.contrib import messages
from datetime import datetime
from happening.configuration import get_configuration_variables, attach_to_form
from happening.configuration import save_variables
from events.utils import dump_preset


@staff_member_required
def index(request):
    """Show the staff index."""
    return render(request, "staff/index.html")


@staff_member_required
def members(request):
    """Administrate members."""
    members = get_user_model().objects.all()
    paginator = Paginator(members, 10)

    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        members = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        members = paginator.page(paginator.num_pages)
    return render(request, "staff/members.html", {"members": members})


@staff_member_required
def make_staff(request, pk):
    """Make a member staff."""
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == "POST":
        messages.success(request, "%s has been made staff" % user)
        user.is_staff = True
        user.save()
    return redirect("staff_members")


@staff_member_required
def make_not_staff(request, pk):
    """Make a member not staff."""
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == "POST":
        messages.success(request, "%s has been made not staff" % user)
        user.is_staff = False
        user.save()
    return redirect("staff_members")


@staff_member_required
def events(request):
    """Administrate events."""
    events = Event.objects.all().order_by('-datetime')
    paginator = Paginator(events, 10)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    return render(request, "staff/events.html", {"events": events})


@staff_member_required
def event_presets(request):
    """Administrate event presets."""
    presets = EventPreset.objects.all()
    return render(request, "staff/event_presets.html", {"presets": presets})


@staff_member_required
def edit_event_preset(request, pk):
    """Edit an event preset."""
    preset = get_object_or_404(EventPreset, pk=pk)
    value = preset.value_as_dict()
    form = EventForm(initial=value)
    variables = get_configuration_variables("event_configuration")
    if request.method == "POST":
        form = EventForm(request.POST, initial=value)
        attach_to_form(form, variables)
        form.is_valid()
        preset_name = request.POST.get("preset_name")
        if not preset_name:
            preset_name = "Preset %s" % (EventPreset.objects.count() +
                                         1)
        preset.name = preset_name
        preset.value = dump_preset(form.cleaned_data)
        preset.save()
        messages.success(request, "%s updated." % preset)
        return redirect("event_presets")
    else:
        attach_to_form(form, variables)
    return render(request, "staff/edit_event_preset.html",
                  {"preset": preset, "form": form})


@staff_member_required
def delete_event_preset(request, pk):
    """Delete an event preset."""
    preset = get_object_or_404(EventPreset, pk=pk)
    if request.method == "POST":
        messages.success(request, "%s deleted" % preset)
        preset.delete()
    return redirect("event_presets")


@staff_member_required
def create_event_preset(request):
    """Create an event preset."""
    form = EventForm()
    variables = get_configuration_variables("event_configuration")
    if request.method == "POST":
        form = EventForm(request.POST)
        attach_to_form(form, variables)
        form.is_valid()
        preset_name = request.POST.get("preset_name")
        if not preset_name:
            preset_name = "Preset %s" % (EventPreset.objects.count() +
                                         1)
        preset = EventPreset(name=preset_name)
        preset.value = dump_preset(form.cleaned_data)
        preset.save()
        messages.success(request, "%s created." % preset)
        return redirect("event_presets")
    else:
        attach_to_form(form, variables)
    return render(request, "staff/create_event_preset.html",
                  {"form": form})


@staff_member_required
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

    return render(request, "staff/add_attendee.html",
                  {"event": event,
                   "members": members})


@staff_member_required
def check_in(request, pk):
    """Check in a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if not ticket.checked_in:
        ticket.checked_in = True
        ticket.checked_in_datetime = datetime.now()
        ticket.save()
        messages.success(request, ticket.user.name() + " has been checked in.")
    return redirect(request.GET.get("redirect_to"))


@staff_member_required
def cancel_check_in(request, pk):
    """Cancel the check in for a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.checked_in:
        ticket.checked_in = False
        ticket.checked_in_datetime = datetime.now()
        ticket.save()
        messages.success(request, ticket.user.name() +
                         " is no longer checked in.")
    return redirect(request.GET.get("redirect_to"))


@staff_member_required
def manage_check_ins(request, pk):
    """Manage check ins."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "staff/manage_check_ins.html", {"event": event})


@staff_member_required
def event(request, pk):
    """View event."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "staff/event.html", {"event": event})


@staff_member_required
def edit_event(request, pk):
    """Edit event."""
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    variables = get_configuration_variables("event_configuration", event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        attach_to_form(form, variables)
        if form.is_valid():
            save_variables(form, variables)
            form.save()
            return redirect("staff_event", event.pk)
    else:
        attach_to_form(form, variables)
    return render(request, "staff/edit_event.html",
                  {"event": event, "form": form})


@staff_member_required
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
    return render(request, "staff/create_event.html",
                  {"form": form,
                   "event_presets": EventPreset.objects.all()})


@staff_member_required
def email_event(request, pk):
    """Send an email to attendees."""
    event = get_object_or_404(Event, pk=pk)
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            # Send email to attendees
            for user in event.attending_users():
                kwargs = {"event_name": str(event),
                          "subject": form.cleaned_data.get("subject"),
                          "message": form.cleaned_data['content']}
                n = AdminEventMessageNotification(user, **kwargs)
                n.send()
            return redirect("staff_events")
    return render(request, "staff/email_event.html",
                  {"event": event, "form": form})


@staff_member_required
def send_email(request):
    """Send an email to all members."""
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            # Send email to members
            for user in get_user_model().objects.filter(is_active=True):
                n = AdminMessageNotification(
                    user,
                    subject=form.cleaned_data.get("subject"),
                    message=form.cleaned_data['content'])
                n.send()
            return redirect("staff_send_email")
    return render(request, "staff/send_email.html",
                  {"form": form})


@staff_member_required
def get_vote_winner(request, pk):
    """Get an AJAX response of the winning language for an event."""
    event = get_object_or_404(Event, pk=pk)
    return HttpResponse(json.dumps({"value": event.winning_language}),
                        content_type="application/json")


@staff_member_required
def pages(request):
    """Administrate pages."""
    pages = Page.objects.all()
    paginator = Paginator(pages, 10)

    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pages = paginator.page(paginator.num_pages)
    return render(request, "staff/pages.html", {"pages": pages})


@staff_member_required
def edit_page(request, pk):
    """Edit page."""
    page = get_object_or_404(Page, pk=pk)
    form = PageForm(instance=page)
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("staff_pages")
    return render(request, "staff/edit_page.html",
                  {"page": page, "form": form})


@staff_member_required
def delete_page(request, pk):
    """Delete page."""
    page = get_object_or_404(Page, pk=pk)
    page.delete()
    return redirect("staff_pages")


@staff_member_required
def create_page(request):
    """Create page."""
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page created.')
            return redirect("staff_pages")
    return render(request, "staff/create_page.html", {"form": form})
