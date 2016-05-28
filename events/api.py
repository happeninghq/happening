from models import Event, TicketType, TicketOrder, Ticket
from serializers import EventSerializer, TicketTypeSerializer
from serializers import TicketSerializer, TicketOrderSerializer
from happening.api import Api


class EventApi(Api):
    """Event API."""

    model = Event
    serializer_class = EventSerializer


class TicketTypeApi(Api):
    """Ticket Type API."""

    model = TicketType
    serializer_class = TicketTypeSerializer


class TicketApi(Api):
    """Ticket API."""

    model = Ticket
    serializer_class = TicketSerializer


class TicketOrderApi(Api):
    """Ticket Order API."""

    model = TicketOrder
    serializer_class = TicketOrderSerializer
