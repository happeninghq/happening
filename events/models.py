"""Event models."""
from django.db import models
from happening import db
from django.utils import timezone
from exceptions import EventFinishedError, NoTicketsError
from datetime import datetime, timedelta
import pytz
from happening.utils import custom_strftime
import random
from django.core.urlresolvers import reverse
from notifications import CancelledTicketNotification
from notifications import PurchasedTicketNotification
from django.conf import settings
from happening.plugins import trigger_action
import json
from happening.db import AddressField
from happening.storage import media_path


class Event(db.Model):

    """An event."""

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    title = models.CharField(max_length=255)

    # The number of tickets available in total for this event
    available_tickets = models.IntegerField(default=30)

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
    def recommended_languages(self):
        """Return all languages suggested so far."""
        all_votes = [t.default_votes for t in self.tickets.all()
                     if t.default_votes is not None]
        # Flatten the list
        all_votes = list(set([item for sublist in all_votes
                              for item in sublist]))
        random.shuffle(all_votes)
        return all_votes

    @property
    def taken_tickets(self):
        """Return the number of tickets purchased."""
        return self.tickets.filter(cancelled=False).count()

    @property
    def remaining_tickets(self):
        """Return the number of tickets available to purchase."""
        return self.available_tickets - self.taken_tickets

    @property
    def is_future(self):
        """Return True if this event is in the future. False otherwise."""
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

    def buy_ticket(self, user, tickets=1):
        """Buy the given number of tickets for the given user."""
        if not self.is_future:
            raise EventFinishedError()

        if self.remaining_tickets < tickets:
            raise NoTicketsError()

        order = TicketOrder(user=user, event=self)
        order.save()

        for i in range(tickets):
            ticket = Ticket(event=self, user=user, order=order)
            ticket.save()

        kwargs = {"order": order,
                  "tickets_count": order.tickets.count(),
                  "event": self,
                  "event_name": str(self)}

        n = PurchasedTicketNotification(
            user,
            **kwargs)
        n.send()

        return order

    def attending_users(self):
        """Get a list of attending users."""
        return set([t.user for t in self.tickets.all() if not t.cancelled])

    def __unicode__(self):
        """Return the title of this event."""
        return self.title


class TicketOrder(db.Model):

    """A ticket order."""

    event = models.ForeignKey(Event, related_name="orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders")
    purchased_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def cancelled(self):
        """Have all tickets in this order been cancelled."""
        return all([t.cancelled for t in self.tickets.all()])


class Ticket(db.Model):

    """A claim by a user on a place at an event."""

    event = models.ForeignKey(Event, related_name="tickets")
    # This is nullable until things have been migrated
    order = models.ForeignKey(TicketOrder, related_name="tickets", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tickets")
    cancelled = models.BooleanField(default=False)
    cancelled_datetime = models.DateTimeField(blank=True, null=True)

    checked_in = models.BooleanField(default=False)
    checked_in_datetime = models.DateTimeField(blank=True, null=True)

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
