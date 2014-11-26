""" Event models. """
from django.db import models
from sponsorship.models import Sponsor
from django.utils import timezone
from exceptions import DojoFinishedError, NoTicketsError
from exceptions import TicketCancelledError


class EventManager(models.Manager):

    """ Custom Event Manager, to add site-wide functionality. """

    def latest_event(self):
        """ Get the latest event.

        This will be either the next one in future or the most recent one
        if there are no future events.
        """
        next_event = self.filter(
            datetime__gte=timezone.now()).order_by("datetime").first()
        if next_event:
            return next_event
        return self.order_by("-datetime").first()


class Event(models.Model):

    """ A code dojo event. """

    objects = EventManager()

    datetime = models.DateTimeField()

    # This can be null if this event isn't sponsored
    sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

    # The number of tickets available in total for this event
    available_tickets = models.IntegerField()

    # If completed, this information will be used on the "info" page
    challenge_language = models.CharField(max_length=200, blank=True,
                                          null=True)
    challenge_title = models.CharField(max_length=200, blank=True, null=True)

    challenge_text = models.TextField(blank=True, null=True)
    solution_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="event_images", blank=True, null=True)

    @property
    def remaining_tickets(self):
        """ Return the number of tickets available to purchase. """
        taken_tickets = sum(
            [t.number for t in self.tickets.all() if not t.cancelled])
        return self.available_tickets - taken_tickets

    def is_future(self):
        """ Return True if this event is in the future. False otherwise. """
        return self.datetime > timezone.now()

    def challenge(self):
        """ Return the language and challenge if available. """
        if self.challenge_language and self.challenge_title:
            return "%s %s" % (self.challenge_language, self.challenge_title)
        elif self.challenge_title:
            return self.challenge_title
        elif self.challenge_language:
            return self.challenge_language
        return None

    def heading(self):
        """ Return the title and challenge. """
        s = self.__unicode__()
        if self.challenge():
            s += " (%s)" % self.challenge()
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def year_heading(self):
        """ Return the month, year, and challenge. """
        s = self.month_year()
        if self.challenge():
            s += " (%s)" % self.challenge()
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def month_year(self):
        """ Return the month and year. """
        return self.datetime.strftime("%B %Y")

    def buy_ticket(self, user, tickets=1):
        """ Buy the given number of tickets for the given user. """
        if not self.is_future():
            raise DojoFinishedError()
        if self.remaining_tickets == 0:
            raise NoTicketsError()
        ticket = Ticket(event=self, user=user, number=tickets)
        ticket.save()
        return ticket

    def __unicode__(self):
        """ Return the title of this dojo. """
        return "%s Code Dojo" % self.datetime.strftime("%B")


class EventSolution(models.Model):

    """ A solution from a team at a dojo. """

    event = models.ForeignKey(Event, related_name="solutions")
    team_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    github_url = models.URLField()

    @property
    def name(self):
        """ Return the team name, or team number if there is none. """
        return self.team_name if self.team_name else "No Name"  # TODO

    def __unicode__(self):
        """ Return the title of this solution. """
        return "%s %s" % (self.event, self.team_name)


class Ticket(models.Model):

    """ A claim by a user on a place at an event. """

    event = models.ForeignKey(Event, related_name="tickets")
    user = models.ForeignKey("auth.User", related_name="tickets")
    number = models.IntegerField(default=1)
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    last_edited_datetime = models.DateTimeField(auto_now=True)
    cancelled = models.BooleanField(default=False)
    cancelled_datetime = models.DateTimeField(blank=True, null=True)

    def change_number(self, number):
        """ Change the number on the ticket. """
        if number == 0:
            return self.cancel()

        if not self.event.is_future():
            raise DojoFinishedError()

        if ((self.event.remaining_tickets + self.number) - number) < 0:
            # We've ran out of tickets
            raise NoTicketsError()

        if self.cancelled:
            raise TicketCancelledError()

        self.number = number
        self.save()

    def cancel(self):
        """ Cancel the ticket. """
        if not self.event.is_future():
            raise DojoFinishedError()
        if not self.cancelled:
            self.cancelled = True
            self.cancelled_datetime = timezone.now()
            self.save()
