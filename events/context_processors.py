"""Event-related context processors."""

from events.models import Event


def events(request):
    """Add the last five events to the context."""
    events = Event.objects.all().order_by("-datetime")[:5]
    return {"events": events}
