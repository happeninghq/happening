"""Notification views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import NotificationPreference
from happening import notifications
from django.contrib import messages
from happening.plugins import plugin_enabled
from django.http import Http404
from django.contrib.auth.models import User
from django.core.signing import Signer
signer = Signer()


@login_required()
def list_notifications(request):
    """List all notifications."""
    rendered = render(request, "notifications/list.html")
    for notification in request.user.notifications.all():
        notification.mark_as_read()
    return rendered


def save_settings(request, notification_types):
    """Save the notification settings POSTed."""
    for n in list(notification_types.keys()):
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
    """Convert notification types into a user's formatted settings."""
    categories = {}
    for n, o in list(notification_types.items()):
        if not o.can_edit_send_notification and not o.can_edit_send_email:
            continue

        if o.admin_only and not user.is_superuser:
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


def get_notification_types():
    """Get a list of notification types."""
    notification_types = {}
    for cls in notifications.Notification.__subclasses__():
        path = cls.__module__.split('.')
        if path[0] == 'plugins' and not plugin_enabled("plugins.%s" % path[1]):
            continue
        notification_types[cls.__name__] = cls
    return notification_types


@login_required
def settings(request):
    """Change the user's notification settings."""
    notification_types = get_notification_types()

    if request.method == "POST":
        # Save the preferences
        return save_settings(request, notification_types)

    # Otherwise render the settings
    categories = format_notification_settings(request.user, notification_types)

    return render(request, "notifications/settings.html",
                  {"categories": categories})


def unsubscribe(request):
    """Allow quickly unsubscribing from emails."""
    user_id = request.GET['user']
    notification_name = request.GET['type']
    notification_types = get_notification_types()

    signer.unsign(user_id + ":" + notification_name + ":" +
                  request.GET['signature'])

    if notification_name not in notification_types:
        # Not a valid notification
        raise Http404

    user = get_object_or_404(User, pk=user_id)

    preference = NotificationPreference.objects.filter(
        user=user, notification=notification_name[:-12]).first()

    if preference is not None and not preference.send_emails:
        response = redirect('notifications_unsubscribed')
        response['Location'] += '?user=%s&type=%s&signature=%s' % (
            user_id, notification_name, request.GET['signature'])
        return response

    if request.method == "POST":
        # Do the unsubscribing
        preference, _ = NotificationPreference.objects.get_or_create(
            user=user,
            notification=notification_name[:-12])
        preference.send_emails = False
        preference.save()
        response = redirect('notifications_unsubscribed')
        response['Location'] += '?user=%s&type=%s&signature=%s' % (
            user_id, notification_name, request.GET['signature'])
        return response

    return render(request, "notifications/unsubscribe.html", {
        "user": user,
        "notification_type": notification_name,
        "notification_name": notification_name[:-12],
        "signature": request.GET['signature']
    })


def unsubscribe_all(request):
    """Allow quickly unsubscribing from all emails."""
    user_id = request.GET['user']
    user = get_object_or_404(User, pk=user_id)
    notification_name = request.GET['type']

    signer.unsign(user_id + ":" + notification_name + ":" +
                  request.GET['signature'])

    if request.method == "POST":
        # Do the unsubscribing
        notification_types = get_notification_types()
        for notification_name in notification_types.keys():
            preference, _ = NotificationPreference.objects.get_or_create(
                user=user,
                notification=notification_name[:-12])
            preference.send_emails = False
            preference.save()
        response = redirect('notifications_unsubscribed_all')
        response['Location'] += '?user=%s&type=%s&signature=%s' % (
            user_id, request.GET['type'], request.GET['signature'])
        return response

    return render(request, "notifications/unsubscribe_all.html", {
        "user": user,
        "notification_type": request.GET['type'],
        "signature": request.GET['signature']
    })


def unsubscribed(request):
    """A user has unsubscribed from an email."""
    user_id = request.GET['user']
    notification_name = request.GET['type']
    notification_types = get_notification_types()

    signer.unsign(user_id + ":" + notification_name + ":" +
                  request.GET['signature'])

    if notification_name not in notification_types:
        # Not a valid notification
        raise Http404

    user = get_object_or_404(User, pk=user_id)
    return render(request, "notifications/unsubscribed.html", {
        "user": user,
        "notification_type": notification_name,
        "notification_name": notification_name[:-12],
        "signature": request.GET['signature']
    })


def unsubscribed_all(request):
    """A user has unsubscribed from all emails."""
    user_id = request.GET['user']
    user = get_object_or_404(User, pk=user_id)
    notification_name = request.GET['type']

    signer.unsign(user_id + ":" + notification_name + ":" +
                  request.GET['signature'])
    return render(request, "notifications/unsubscribed_all.html",
                  {"user": user,
                   "notification_type": request.GET['type'],
                   "signature": request.GET['signature']})
