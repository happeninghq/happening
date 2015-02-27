""" Notification views. """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import NotificationPreference
import notifications
import inspect
from django.contrib import messages


@login_required()
def list(request):
    """ List all notifications. """
    rendered = render(request, "notifications/list.html")
    request.user.notifications.mark_all_as_read()
    return rendered


@login_required()
def short(request):
    """ Return rendered list of short notifications. """
    # TODO: Replace this with a JSON request
    # and render client side
    rendered = render(request, "notifications/short.html")
    request.user.notifications.mark_all_as_read()
    return rendered


def save_settings(request, notification_types):
    """ Save the notification settings POSTed. """
    for n in notification_types.keys():
        name = n[:-12]
        preference, _ = NotificationPreference.objects.get_or_create(
            user=request.user,
            notification=name)
        preference.send_notifications = False
        preference.send_emails = False
        if name + "_email" in request.POST:
            preference.send_emails = True
        if name + "_notification" in request.POST:
            preference.send_notifications = True
        preference.save()
    messages.success(request,
                     "Your notification settings have been saved")
    return redirect("notifications_settings")


def format_notification_settings(user, notification_types):
    """ Convert notification types into a user's formatted settings. """
    categories = {}
    for n, o in notification_types.items():
        if not o.can_edit_send_notification and not o.can_edit_send_email:
            continue

        if o.category not in categories:
            categories[o.category] = []

        send_notifications = o.send_notification
        send_emails = o.send_email

        # Check if the user has saved this notification before
        preference = user.notification_preferences.filter(
            notification=n[:-12]).first()
        if preference:
            send_notifications = preference.send_notifications
            send_emails = preference.send_emails

        categories[o.category].append(
            (n[:-12], o.__doc__, o.can_edit_send_notification,
                send_notifications, o.can_edit_send_email, send_emails))
    return categories


@login_required
def settings(request):
    """ Change the user's notification settings. """
    notification_types = {}
    for name, obj in inspect.getmembers(notifications):
        if inspect.isclass(obj):
            if notifications.Notification in obj.__bases__:
                notification_types[name] = obj

    if request.method == "POST":
        # Save the preferences
        return save_settings(request, notification_types)

    # Otherwise render the settings
    categories = format_notification_settings(request.user, notification_types)

    return render(request, "notifications/settings.html",
                  {"categories": categories})
