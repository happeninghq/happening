"""Period tasks related to events."""

from periodically.decorators import hourly
from models import Event
from datetime import datetime, timedelta
import pytz
from django.conf import settings


@hourly()
def send_event_notifications():
    """Send notifications for upcoming events."""
    first_notification_cutoff = datetime.now(pytz.utc) + \
        timedelta(hours=settings.FIRST_NOTIFICATION_TIME)
    second_notification_cutoff = datetime.now(pytz.utc) + \
        timedelta(hours=settings.SECOND_NOTIFICATION_TIME)
    upcoming_events = Event.objects.filter(
        datetime__gt=datetime.now(pytz.utc),
        datetime__lt=first_notification_cutoff)

    for event in upcoming_events:
        if event.datetime < second_notification_cutoff and \
                not event.upcoming_notification_2_sent:
            event.send_upcoming_notification_2()
        elif not event.upcoming_notification_1_sent:
            event.send_upcoming_notification_1()
