""" Event-related context processors. """

from events.models import Event
from django.utils import timezone


def previous_events(request):
    """ Add the last five events to the context. """
    previous_events = Event.objects.filter(
        datetime__lte=timezone.now()).order_by("-datetime")[:5]
    return {"previous_events": previous_events}
