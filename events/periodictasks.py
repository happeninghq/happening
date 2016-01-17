"""Period tasks related to events."""

from periodically.decorators import every
from models import TicketOrder
from payments.models import Payment
from datetime import datetime
from configuration import TicketTimeout


@every(seconds=30)
def timeout_held_tickets():
    """Ensure that held tickets are released."""
    timeout = datetime.now() - TicketTimeout().get()
    for order in TicketOrder.objects.filter(
            purchased_datetime__lt=timeout,
            complete=False):

        # Cancel payment
        payment = Payment.objects.filter(
            _complete=False,
            extra__at_held_tickets_pk=order.pk
            ).first()

        if payment:
            payment.delete()

        # Delete tickets
        for ticket in order.tickets.all():
            ticket.delete()

        # Delete order
        order.delete()
