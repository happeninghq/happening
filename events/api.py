from models import Event, TicketType, TicketOrder, Ticket
from rest_framework import viewsets
from serializers import EventSerializer, TicketTypeSerializer
from serializers import TicketSerializer, TicketOrderSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Event API."""

    queryset = Event.objects.all().order_by('-start')
    serializer_class = EventSerializer


class TicketTypeViewSet(viewsets.ModelViewSet):
    """Ticket Type API."""

    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """Ticket API."""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketOrderViewSet(viewsets.ModelViewSet):
    """Ticket Order API."""

    queryset = TicketOrder.objects.all()
    serializer_class = TicketOrderSerializer
