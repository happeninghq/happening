"""Period tasks related to events."""

from celery.decorators import periodic_task
from datetime import timedelta
from .models import TicketOrder, WaitingListSubscription, TicketType
from payments.models import Payment
from datetime import datetime
from .configuration import TicketTimeout
from events.notifications import WaitingListExpiredNotification


@periodic_task(run_every=timedelta(seconds=30))
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


@periodic_task(run_every=timedelta(minutes=5))
def timeout_waiting_list():
    """Ensure that waiting list subscriptions are removed."""
    for subscription in WaitingListSubscription.objects.filter(
            can_purchase=True,
            can_purchase_expiry__lt=datetime.now()):

        n = WaitingListExpiredNotification(
            subscription.user, event=subscription.ticket_type.event,
            event_name=str(subscription.ticket_type.event))
        n.send()

        subscription.delete()


@periodic_task(run_every=timedelta(minutes=10))
def manage_waiting_list():
    """Ensure that tickets are distributed to waiting lists."""
    def manage_waiting_list_for(ticket_type):
        allowed_to_purchase = ticket_type.waiting_list_subscriptions.filter(
            can_purchase=True).count()

        while ticket_type.remaining_tickets > allowed_to_purchase:
            # Release it to the next person in the queue
            next_person = ticket_type.waiting_list_subscriptions.filter(
                can_purchase=False).first()
            if not next_person:
                # Cannot release any more, continue to next ticket_type
                return
            next_person.set_can_purchase()
            next_person.save()

            allowed_to_purchase += 1

    # TODO: Make this query more specific so we don't waste time
    for ticket_type in TicketType.objects.filter(
            waiting_list_enabled=True,
            waiting_list_automatic=True,
            ):
        manage_waiting_list_for(ticket_type)
