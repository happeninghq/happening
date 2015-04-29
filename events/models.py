"""Event models."""
from django.db import models
from django.utils import timezone
from exceptions import EventFinishedError, NoTicketsError
from exceptions import TicketCancelledError
from datetime import datetime, timedelta
import pytz
from happening.utils import custom_strftime
from jsonfield import JSONField
import random
from django.core.urlresolvers import reverse
from notifications.notifications import EventInformationNotification
from notifications.notifications import CancelledTicketNotification
from notifications.notifications import EditedTicketNotification
from notifications.notifications import PurchasedTicketNotification
from django.conf import settings
from happening.plugins import trigger_action


class EventManager(models.Manager):

    """Custom Event Manager, to add site-wide functionality."""

    def latest_event(self):
        """Get the latest event.

        This will be either the next one in future or the most recent one
        if there are no future events.
        """
        next_event = self.all().filter(
            datetime__gte=timezone.now()).order_by("datetime").first()
        if next_event:
            return next_event
        return self.all().order_by("-datetime").first()


class Event(models.Model):

    """An event."""

    objects = EventManager()

    datetime = models.DateTimeField()

    title = models.CharField(max_length=255)

    # The number of tickets available in total for this event
    available_tickets = models.IntegerField(default=30)

    # If completed, this information will be used on the "info" page
    challenge_language = models.CharField(max_length=200, blank=True,
                                          null=True)
    challenge_title = models.CharField(max_length=200, blank=True, null=True)

    challenge_text = models.TextField(blank=True, null=True)
    solution_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="media/event_images", blank=True,
                              null=True)

    # Has the first "upcoming event" notification been sent?
    upcoming_notification_1_sent = models.BooleanField(default=False)

    # Has the second "upcoming event" notification been sent?
    upcoming_notification_2_sent = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Get the url to the event."""
        return reverse('view_event', kwargs={"pk": self.pk})

    @property
    def time_to_string(self):
        """Return the event time as a humanized string."""
        now = datetime.now(pytz.utc).date()
        other_date = self.datetime.date()

        datestr = custom_strftime("%A %B {S}, %Y", self.datetime)
        shortdate = "(%s)" % custom_strftime("{S}", self.datetime)

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

        time = self.datetime.strftime("%I:%M%p").lstrip("0")
        if self.datetime.minute == 0:
            time = self.datetime.strftime("%I%p").lstrip("0")
        return datestr + " at " + time

    @property
    def previous_event(self):
        """Return the event immediately prior to this one."""
        return Event.objects.all().filter(
            datetime__lt=self.datetime).order_by("-datetime").first()

    @property
    def is_voting(self):
        """Return True if the event is currently accepting language votes."""
        return self.is_future and not self.challenge_language

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
    def winning_language(self):
        """Return the language which has the most votes."""
        from voting import AVVote
        vote = AVVote()
        if self.previous_event and self.previous_event.challenge_language:
            vote = AVVote(ignore=[self.previous_event.challenge_language])
        for ticket in self.tickets.all():
            if ticket.default_votes is not None:
                vote.add_preference(ticket.default_votes)
        return vote.winner

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
        return self.datetime > timezone.now()

    def challenge(self):
        """Return the language and challenge if available."""
        if self.challenge_language and self.challenge_title:
            return "%s %s" % (self.challenge_language, self.challenge_title)
        elif self.challenge_title:
            return self.challenge_title
        elif self.challenge_language:
            return self.challenge_language
        return None

    def heading(self):
        """Return the title and challenge."""
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def year_heading(self):
        """Return the month, year, and challenge."""
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def month_year(self):
        """Return the month and year."""
        return self.datetime.strftime("%B %Y")

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

        # We only send notifications if we haven't already purchased
        # a ticket for this event (otherwise we will already have
        # this notification)
        if created:
            if self.upcoming_notification_2_sent:
                self.send_upcoming_notification_2(user)
            elif self.upcoming_notification_1_sent:
                self.send_upcoming_notification_1(user)

        return ticket

    def attending_users(self):
        """Get a list of attending users."""
        return [t.user for t in self.tickets.all() if not t.cancelled]

    def __unicode__(self):
        """Return the title of this event."""
        return self.title

    def _send_upcoming_notification(self, user, is_final):
        kwargs = {"event": self,
                  "event_name": str(self),
                  "time_to_event": self.time_to_string,
                  "is_voting": self.is_voting,
                  "is_final_notification": is_final
                  }
        e = EventInformationNotification(user, **kwargs)
        e.send()

    def send_upcoming_notification_2(self, user=None):
        """Second the second "upcoming event" notification."""
        if user is None:
            users = set([ticket.user for ticket in self.tickets.all()
                         if not ticket.cancelled])
            for user in users:
                self._send_upcoming_notification(user, True)
            self.upcoming_notification_2_sent = True
            self.upcoming_notification_1_sent = True
            self.save()
        else:
            self._send_upcoming_notification(user, True)

    def send_upcoming_notification_1(self, user=None):
        """Second the first "upcoming event" notification."""
        if user is None:
            users = set([ticket.user for ticket in self.tickets.all()
                         if not ticket.cancelled])
            for user in users:
                self._send_upcoming_notification(user, False)
            self.upcoming_notification_1_sent = True
            self.save()
        else:
            self._send_upcoming_notification(user, False)


class Ticket(models.Model):

    """A claim by a user on a place at an event."""

    event = models.ForeignKey(Event, related_name="tickets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tickets")
    number = models.IntegerField(default=1)
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    last_edited_datetime = models.DateTimeField(auto_now=True)
    cancelled = models.BooleanField(default=False)
    cancelled_datetime = models.DateTimeField(blank=True, null=True)
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
