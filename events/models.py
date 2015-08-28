"""Event models."""
from django.db import models
from happening import db
from django.utils import timezone
from exceptions import EventFinishedError, NoTicketsError
from exceptions import TicketCancelledError
from datetime import datetime, timedelta
import pytz
from happening.utils import custom_strftime
from jsonfield import JSONField
import random
from django.core.urlresolvers import reverse
from notifications import CancelledTicketNotification
from notifications import EditedTicketNotification
from notifications import PurchasedTicketNotification
from django.conf import settings
from happening.plugins import trigger_action
import json
from happening.db import AddressField


class Event(db.Model):

    """An event."""

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    title = models.CharField(max_length=255)

    # The number of tickets available in total for this event
    available_tickets = models.IntegerField(default=30)

    image = models.ImageField(upload_to="events", null=True)
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
        return sum(
            [t.number for t in self.tickets.all() if not t.cancelled])

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

        # First check if they already have tickets - in which case just
        # add this ticket to theirs

        ticket, created = Ticket.objects.get_or_create(event=self, user=user,
                                                       cancelled=False)
        if created:
            ticket.number = tickets
        else:
            ticket.number += tickets
        ticket.save()

        kwargs = {"ticket": ticket,
                  "event": self,
                  "event_name": str(self)}

        n = PurchasedTicketNotification(
            user,
            **kwargs)
        n.send()

        return ticket

    def attending_users(self):
        """Get a list of attending users."""
        return [t.user for t in self.tickets.all() if not t.cancelled]

    def __unicode__(self):
        """Return the title of this event."""
        return self.title


class Ticket(db.Model):

    """A claim by a user on a place at an event."""

    event = models.ForeignKey(Event, related_name="tickets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tickets")
    number = models.IntegerField(default=1)
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    last_edited_datetime = models.DateTimeField(auto_now=True)
    cancelled = models.BooleanField(default=False)
    cancelled_datetime = models.DateTimeField(blank=True, null=True)
    checked_in = models.BooleanField(default=False)
    checked_in_datetime = models.DateTimeField(blank=True, null=True)
    did_not_attend = models.NullBooleanField()
    votes = JSONField(null=True)

    @property
    def default_votes(self):
        """Return the votes for this event, or previous event."""
        if self.votes is not None:
            return self.votes

        # Otherwise find if we have a previous ticket
        previous_tickets = self.user.tickets.filter(
            cancelled=False,
            purchased_datetime__lt=self.purchased_datetime).order_by(
            '-purchased_datetime')
        if len(previous_tickets) == 0:
            return None
        return previous_tickets[0].default_votes

    def change_number(self, number):
        """Change the number on the ticket."""
        if number == 0:
            return self.cancel()

        if not self.event.is_future:
            raise EventFinishedError()

        if ((self.event.remaining_tickets + self.number) - number) < 0:
            # We've ran out of tickets
            raise NoTicketsError()

        if self.cancelled:
            raise TicketCancelledError()

        self.number = number
        self.save()
        kwargs = {"ticket": self,
                  "event": self.event,
                  "event_name": str(self.event)}

        n = EditedTicketNotification(
            self.user,
            **kwargs)
        n.send()

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
        """Return the ."""
        return "%s's ticket to %s" % (self.user, self.event)


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
