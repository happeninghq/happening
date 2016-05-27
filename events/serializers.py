from models import Event, TicketType, TicketOrder, Ticket
from rest_framework import serializers
from happening.serializers import Serializer


class TicketTypeSerializer(Serializer):
    """Ticket Type Serializer."""

    class Meta:
        model = TicketType
        fields = ('url', 'name', 'number')


class TicketSerializer(Serializer):
    """Ticket Serializer."""

    class Meta:
        model = Ticket
        fields = ('url', 'cancelled', 'checked_in', 'order')


class TicketOrderSerializer(Serializer):
    """Ticket Order Serializer."""

    class Meta:
        model = TicketOrder
        fields = ('url', 'complete', 'purchased_datetime', 'event', 'tickets')

    tickets = TicketSerializer(many=True, read_only=True)


class EventSerializer(Serializer):
    """Event Serializer."""

    configuration_variables = 'event_configuration'

    class Meta:
        model = Event
        fields = ('url', 'start', 'end', 'title', 'image', 'location',
                  'ticket_types', 'ticket_orders', 'tickets')

    location = serializers.JSONField()
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    ticket_orders = TicketOrderSerializer(many=True, read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
