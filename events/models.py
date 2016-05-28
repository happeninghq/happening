"""Event models."""
from django.db import models
from happening import db
from django.utils import timezone
from exceptions import EventFinishedError, NoTicketsError
from datetime import datetime, timedelta
import pytz
from happening.utils import custom_strftime, human_delta
from django.core.urlresolvers import reverse
from notifications import CancelledTicketNotification
from notifications import PurchasedTicketNotification
from notifications import CanPurchaseFromWaitingListNotification
from django.conf import settings
from happening.plugins import trigger_action
import json
from happening.db import AddressField
from happening.storage import media_path
from django.contrib.auth.models import User
from happening import filtering


class Event(db.Model):

    """An event."""

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    title = models.CharField(max_length=255)

    image = models.ImageField(upload_to=media_path("events"), null=True)
    location = AddressField(null=True)

    def get_absolute_url(self):
        """Get the url to the event."""
        return reverse('view_event', kwargs={"pk": self.pk})

    @property
    def time_to_string(self):
        """Return the event time as a humanized string."""
        now = datetime.now(pytz.utc).date()
        other_date = self.start.date()

        datestr = custom_strftime("%A %B {S}, %Y", self.start)
        shortdate = "(%s)" % custom_strftime("{S}", self.start)

        if now == other_date:
            datestr = "today %s" % shortdate
        elif other_date == now - timedelta(days=1):
            datestr = "yesterday %s" % shortdate
        elif other_date == now + timedelta(days=1):
            datestr = "tomorrow %s" % shortdate
        elif now < other_date < now + timedelta(days=7):
            datestr = "next " + other_date.strftime("%A") + " %s" % shortdate
        elif now > other_date > now - timedelta(days=7):
            datestr = "last " + other_date.strftime("%A") + " %s" % shortdate

        time = self.start.strftime("%I:%M%p").lstrip("0")
        if self.start.minute == 0:
            time = self.start.strftime("%I%p").lstrip("0")
        return datestr + " at " + time

    @property
    def previous_event(self):
        """Return the event immediately prior to this one."""
        return Event.objects.all().filter(
            start__lt=self.start).order_by("-start").first()

    @property
    def is_future(self):
        """Return True if this event is in the future. False otherwise."""
        if self.end:
            return self.end > timezone.now()
        return self.start > timezone.now()

    @property
    def date_range(self):
        """Return the formatted date range."""
        if self.end:
            if self.start.date() == self.end.date():
                return self.start.strftime("%b. %d, %Y, %H:%M") +\
                    "-" + self.end.strftime("%H:%M")
            return self.start.strftime("%b. %d, %Y, %H:%M") +\
                '-' + self.end.strftime("%b. %d, %Y, %H:%M")
        return self.start.strftime("%b. %d, %Y, %H:%M")

    def buy_tickets(self, user, tickets):
        """Buy the tickets for the given user.

        tickets should be a dict mapping ticket types to amounts.
        """
        order = self.hold_tickets(user, tickets)
        order.mark_complete()

        return order

    def hold_tickets(self, user, tickets):
        """Hold the tickets for the given user.

        These tickets will expire after 5 minutes.
        """
        if not self.is_future:
            raise EventFinishedError()

        # First verify we have enough tickets
        tickets = {TicketType.objects.get(pk=pk): number for pk, number
                   in tickets.items()}
        for ticket, number in tickets.items():
            if not ticket.event == self:
                raise Exception("Incorrect event")
            if number > ticket.remaining_tickets:
                # ERROR
                raise NoTicketsError()

        # Then create the order
        order = TicketOrder(user=user, event=self)
        order.save()

        # And add the tickets
        for type, number in tickets.items():
            for i in range(number):
                ticket = Ticket(event=self, user=user, order=order,
                                type=type)
                ticket.save()

        return order

    def total_ticket_cost(self, tickets):
        """Sum up total ticket cost."""
        tickets = {TicketType.objects.get(pk=pk): number for pk, number
                   in tickets.items()}
        cost = 0
        for ticket, number in tickets.items():
            if not ticket.event == self:
                raise Exception("Incorrect event")
            cost += ticket.price * number

        return cost

    @property
    def cancelled_tickets(self):
        """List cancelled tickets."""
        return self.tickets.filter(cancelled=True)

    @property
    def total_sold_tickets(self):
        """Get total number of sold tickets."""
        return self.tickets.filter(cancelled=False,
                                   order__complete=True).count()

    @property
    def total_available_tickets(self):
        """Get number of purchasable tickets."""
        return sum(t.number for t in
                   self.ticket_types.active())

    def attending_users(self):
        """Get a list of attending users."""
        return set([t.user for t in self.tickets.all() if
                    (not t.order or t.order.complete) and not t.cancelled])

    def __unicode__(self):
        """Return the title of this event."""
        return self.title


class TicketTypeManager(models.Manager):

    """Custom TicketType manager."""

    def active(self):
        """Get active ticket types."""
        return self.filter(visible=True)

    def visible_to(self, user):
        """Get active ticket types."""
        return [t for t in self.active() if t.visible_to(user)]

    def purchasable_by(self, user):
        """Get purchasable tickets."""
        return [t for t in self.active() if t.purchasable_by(user)]

    def purchasable(self):
        """Get purchasable ticket types."""
        return [t for t in self.active() if t.remaining_tickets > 0]

    def waiting_list_available(self):
        """Get ticket types not purchasable but with waiting list."""
        return [t for t in self.active() if
                t.waiting_list_enabled and (t.remaining_tickets == 0 or
                t.waiting_list_subscriptions.count() > 0)]


class TicketType(db.Model):

    """A type of ticket which can be purchased."""

    objects = TicketTypeManager()

    event = models.ForeignKey(Event, related_name="ticket_types")
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    price = models.IntegerField()
    visible = models.BooleanField(default=False)
    waiting_list_enabled = models.BooleanField(default=False)
    waiting_list_automatic = models.BooleanField(default=False)
    restriction_enabled = models.BooleanField(default=False)
    restriction_filter = models.TextField(null=True)

    @property
    def sold_tickets(self):
        """List of sold tickets."""
        return self.tickets.filter(cancelled=False)

    @property
    def remaining_tickets(self):
        """How many tickets of this time are unsold."""
        return max(0, self.number - self.sold_tickets.count())

    def waiting_list_contains(self, user):
        """True if the waiting list contains the given user."""
        if not user.is_authenticated():
            return False
        if not self.waiting_list_enabled:
            return False
        return self.waiting_list_subscriptions.filter(user=user).count() > 0

    def join_waiting_list(self, user):
        """Add a user to the waiting list."""
        if self.waiting_list_enabled and not self.waiting_list_contains(user)\
                and self.visible_to(user):
            WaitingListSubscription(user=user, ticket_type=self).save()

    def leave_waiting_list(self, user):
        """Remove a user from the waiting list."""
        if self.waiting_list_contains(user):
            for subscription in self.waiting_list_subscriptions.filter(
                    user=user):
                subscription.delete()

    def purchasable_by(self, user):
        """Check that a user is allowed to purchase this ticket."""
        # This will return false if there is a waiting list for example
        if not self.visible_to(user):
            return False
        if self.waiting_list_enabled and\
                self.waiting_list_subscriptions.count() > 0:
            if not user.is_authenticated():
                return False
            waiting_list_subscription = self.waiting_list_subscriptions.filter(
                user=user, can_purchase=True).first()
            return waiting_list_subscription is not None
        return True

    def visible_to(self, user):
        """Check that a user is allowed to see this ticket."""
        if not self.visible:
            return False
        if not self.restriction_enabled:
            return True
        return filtering.matches(user, self.restriction_filter)


class TicketOrderManager(db.Manager):

    """Manager for ticket orders."""

    def get_for_user(self, user):
        """Get the ticket orders visible to the given user."""
        return self.filter(user=user)


class TicketOrder(db.Model):

    """A ticket order."""

    objects = TicketOrderManager()
    event = models.ForeignKey(Event, related_name="orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders")
    complete = models.BooleanField(default=False)
    purchased_datetime = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def has_read_permission(request):
        """All users can read ticket orders."""
        return True

    def has_object_read_permission(self, request):
        """User can only read their own ticket orders."""
        return self.user == request.user

    @property
    def cancelled(self):
        """Have all tickets in this order been cancelled."""
        return all([t.cancelled for t in self.tickets.all()])

    def mark_complete(self):
        """Complete the purchase of a ticket."""
        kwargs = {"order": self,
                  "tickets_count": self.tickets.count(),
                  "event": self.event,
                  "event_name": str(self.event)}

        n = PurchasedTicketNotification(
            self.user,
            **kwargs)
        n.send()

        self.complete = True
        self.save()

        # If this was purchased by someone on a waiting list - remove
        # them from the waiting list

        for t in self.tickets.all():
            subscription = t.type.waiting_list_subscriptions.filter(
                user=self.user).first()
            if subscription:
                subscription.delete()
                # TODO: Maybe record as completed rather than deleting?

            # If there are no tickets left but still people on the waiting list
            # remove their right to buy (so they don't get removed completely)
            if t.type.remaining_tickets == 0:
                for subscription in t.type.waiting_list_subscriptions.filter(
                        can_purchase=True):
                    subscription.can_purchase = False
                    subscription.can_purchase_expiry = None
                    subscription.save()


class TicketManager(db.Manager):

    """Manager for tickets."""

    def get_for_user(self, user):
        """Get the users own tickets."""
        return self.filter(user=user)


class Ticket(db.Model):

    """A claim by a user on a place at an event."""

    objects = TicketManager()
    event = models.ForeignKey(Event, related_name="tickets")
    # This is nullable until things have been migrated
    type = models.ForeignKey(TicketType, related_name="tickets", null=True)
    # This is nullable until things have been migrated
    order = models.ForeignKey(TicketOrder, related_name="tickets", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tickets")
    cancelled = models.BooleanField(default=False)
    cancelled_datetime = models.DateTimeField(blank=True, null=True)

    checked_in = models.BooleanField(default=False)
    checked_in_datetime = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def has_read_permission(request):
        """User can view tickets."""
        return True

    def has_object_read_permission(self, request):
        """User can only view their own tickets."""
        return self.user == request.user

    def cancel(self):
        """Cancel the ticket."""
        if not self.event.is_future:
            raise EventFinishedError()
        if not self.cancelled:
            self.cancelled = True
            self.cancelled_datetime = timezone.now()
            self.save()

            trigger_action("events.ticket_cancelled", ticket=self)

            kwargs = {"ticket": self,
                      "event": self.event,
                      "event_name": str(self.event)}

            n = CancelledTicketNotification(
                self.user,
                **kwargs)
            n.send()

    def __unicode__(self):
        """Return the name."""
        return "%s's ticket to %s" % (self.order.user, self.event)


def member_uncancelled_tickets(member):
    """List the number of tickets not cancelled."""
    return member.tickets.filter(cancelled=False).count()

User.uncancelled_tickets = member_uncancelled_tickets


def member_attended_tickets(member):
    """List the number of attended events."""
    return member.tickets.filter(cancelled=False, checked_in=True).count()

User.attended_tickets = member_attended_tickets


class EventPreset(db.Model):

    """Common settings to be loaded when creating a new event."""

    name = models.CharField(max_length=255)
    value = models.TextField()

    def __unicode__(self):
        """Return the event preset name."""
        return self.name

    def value_as_dict(self):
        """Get the preset value as a dict."""
        return json.loads(self.value)


class WaitingListSubscription(db.Model):

    """A user's subscription to a waiting list."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="waiting_lists")
    ticket_type = models.ForeignKey(TicketType,
                                    related_name="waiting_list_subscriptions")

    can_purchase = models.BooleanField(default=False)
    can_purchase_expiry = models.DateTimeField(null=True)

    def set_can_purchase(self):
        """Mark that this person can purchase a ticket."""
        from events.configuration import WaitingListTimeout
        self.can_purchase = True
        self.can_purchase_expiry = timezone.now() + WaitingListTimeout().get()

        n = CanPurchaseFromWaitingListNotification(
            self.user, event=self.ticket_type.event,
            event_name=str(self.ticket_type.event),
            timeout=human_delta(WaitingListTimeout().get()))
        n.send()

        self.save()
