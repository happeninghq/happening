"""Staff views."""
from happening.utils import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from events.models import Event, Ticket, EventPreset, TicketType
from events.forms import EventForm
from pages.models import Page
from pages.forms import PageForm
from forms import EmailForm
from django.contrib import messages
from django.utils import timezone
from happening.configuration import get_configuration_variables, attach_to_form
from happening.configuration import save_variables
from events.utils import dump_preset
from emails.models import Email
from django.views.decorators.http import require_POST
from emails import render_email
from markdown_deux import markdown
from django.http import JsonResponse
from django.utils import formats


@staff_member_required
def index(request):
    """Show the staff index."""
    return render(request, "staff/index.html")


@staff_member_required
def members(request):
    """Administrate members."""
    members = get_user_model().objects.all()
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
    events = Event.objects.all().order_by('-start')
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
        ticket.checked_in_datetime = timezone.now()
        ticket.save()
        if not request.is_ajax:
            messages.success(request, ticket.user.name() +
                             " has been checked in.")
    if request.is_ajax:
        return JsonResponse({"checked-in": "True<br /> " +
                            formats.date_format(
                                ticket.checked_in_datetime,
                                "DATETIME_FORMAT")})
    return redirect(request.GET.get("next"))


@staff_member_required
def cancel_check_in(request, pk):
    """Cancel the check in for a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.checked_in:
        ticket.checked_in = False
        ticket.checked_in_datetime = timezone.now()
        ticket.save()
        if not request.is_ajax:
            messages.success(request, ticket.user.name() +
                             " is no longer checked in.")

    if request.is_ajax:
        return JsonResponse({"checked-in": "False"})
    return redirect(request.GET.get("next"))


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
        attach_to_form(form, variables, editing=True)
        if form.is_valid():
            form.save()
            save_variables(form, variables)
            return redirect("staff_event", event.pk)
    else:
        attach_to_form(form, variables, editing=True)
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
def manage_waiting_list(request, pk):
    """Manage waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    return render(request, "staff/manage_waiting_list.html",
                  {"ticket_type": ticket_type})


@staff_member_required
def remove_from_waiting_list(request, pk, user_pk):
    """Remove a user from a waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)
    ticket_type.leave_waiting_list(user)

    messages.success(request,
                     "%s has been removed from the waiting list." % user)

    return redirect("manage_waiting_list", pk)


@staff_member_required
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


@staff_member_required
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
            # Send email to attendees
            email = Email(
                to=form.cleaned_data['to'],
                subject=form.cleaned_data['subject'],
                content=form.cleaned_data['content'],
                start_sending=form.cleaned_data['start_sending'],
                stop_sending=form.cleaned_data['stop_sending'],
            )
            email.save()
            messages.success(request, "Email created")
            return redirect("staff_emails")
    return render(request, "staff/email_event.html",
                  {"event": event, "form": form})


@staff_member_required
def pages(request):
    """Administrate pages."""
    pages = Page.objects.all()
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


@staff_member_required
def staff_emails(request):
    """List emails."""
    return render(request,
                  "staff/emails.html",
                  {"emails": Email.objects.all()})


@staff_member_required
def email(request, pk):
    """Show email details."""
    email = get_object_or_404(Email, pk=pk)
    return render(request,
                  "staff/email.html",
                  {"email": email})


@staff_member_required
def create_email(request):
    """Send an email."""
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Email created")
            return redirect("staff_emails")
    return render(request, "staff/create_email.html",
                  {"form": form})


@staff_member_required
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
    return render(request, "staff/edit_email.html",
                  {"form": form, "email": email})


@staff_member_required
def disable_email(request, pk):
    """Disable an email."""
    email = get_object_or_404(Email, pk=pk)
    email.disabled = True
    email.save()
    messages.success(request, "The email has been disabled")
    return redirect(request.GET.get("redirect", "staff_emails"))


@staff_member_required
def enable_email(request, pk):
    """Enable an email."""
    email = get_object_or_404(Email, pk=pk)
    email.disabled = False
    email.save()
    messages.success(request, "The email has been enabled")
    return redirect(request.GET.get("redirect", "staff_emails"))


@staff_member_required
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
