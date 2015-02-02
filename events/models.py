""" Event models. """
from django.db import models
from sponsorship.models import Sponsor
from django.utils import timezone
from exceptions import DojoFinishedError, NoTicketsError
from exceptions import TicketCancelledError
from datetime import datetime, timedelta
import pytz
from website.utils import custom_strftime
from jsonfield import JSONField
import random


class EventManager(models.Manager):

    """ Custom Event Manager, to add site-wide functionality. """

    def latest_event(self):
        """ Get the latest event.

        This will be either the next one in future or the most recent one
        if there are no future events.
        """
        next_event = self.all().filter(
            datetime__gte=timezone.now()).order_by("datetime").first()
        if next_event:
            return next_event
        return self.all().order_by("-datetime").first()


class Event(models.Model):

    """ A code dojo event. """

    objects = EventManager()

    datetime = models.DateTimeField()

    # This can be null if this event isn't sponsored
    sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

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

    @property
    def time_to_string(self):
        """ Return the event time as a humanized string. """
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

    def ordered_solutions(self):
        """ Return solutions sorted by group number. """
        return self.solutions.all().order_by('team_number')

    @property
    def is_voting(self):
        """ Return True if the event is currently accepting language votes. """
        return self.is_future and not self.challenge_language

    @property
    def recommended_languages(self):
        """ Return all languages suggested so far. """
        all_votes = [t.votes for t in self.tickets.all()
                     if t.votes is not None]
        # Flatten the list
        all_votes = list(set([item for sublist in all_votes
                              for item in sublist]))
        random.shuffle(all_votes)
        return all_votes

    @property
    def winning_language(self):
        """ Return the language which has the most votes. """
        from voting import AVVote
        vote = AVVote()
        for ticket in self.tickets.all():
            if ticket.votes is not None:
                vote.add_preference(ticket.votes)
        return vote.winner

    @property
    def remaining_tickets(self):
        """ Return the number of tickets available to purchase. """
        taken_tickets = sum(
            [t.number for t in self.tickets.all() if not t.cancelled])
        return self.available_tickets - taken_tickets

    @property
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
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def year_heading(self):
        """ Return the month, year, and challenge. """
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def month_year(self):
        """ Return the month and year. """
        return self.datetime.strftime("%B %Y")

    def buy_ticket(self, user, tickets=1):
        """ Buy the given number of tickets for the given user. """
        if not self.is_future:
            raise DojoFinishedError()

        if self.remaining_tickets < tickets:
            raise NoTicketsError()

        # First check if they already have tickets - in which case just
        # add this ticket to theirs

        ticket = Ticket(event=self, user=user, number=tickets)
        ticket.save()

        user.send_email("events/registered_for_event", {"ticket": ticket})

        # We only send notifications if we haven't already purchased
        # a ticket for this event (otherwise we will already have
        # this notification)
        num_tickets = len([t for t in self.tickets.all() if t.user == user])
        if num_tickets == 1:
            if self.upcoming_notification_2_sent:
                self.send_upcoming_notification_2(user)
            elif self.upcoming_notification_1_sent:
                self.send_upcoming_notification_1(user)

        return ticket

    def attending_users(self):
        """ Get a list of attending users.

        Guaranteed unique, even if they purchase multiple tickets.
        """
        return set([t.user for t in self.tickets.all() if not t.cancelled])

    def __unicode__(self):
        """ Return the title of this dojo. """
        return "%s Code Dojo" % self.datetime.strftime("%B")

    def send_upcoming_notification_2(self, user=None):
        """ Second the second "upcoming event" notification. """
        if user is None:
            users = set([ticket.user for ticket in self.tickets.all()
                         if not ticket.cancelled])
            for user in users:
                user.send_email("events/upcoming_2", {"event": self})
            self.upcoming_notification_2_sent = True
            self.upcoming_notification_1_sent = True
            self.save()
        else:
            user.send_email("events/upcoming_2", {"event": self})

    def send_upcoming_notification_1(self, user=None):
        """ Second the first "upcoming event" notification. """
        if user is None:
            users = set([ticket.user for ticket in self.tickets.all()
                         if not ticket.cancelled])
            for user in users:
                user.send_email("events/upcoming_1", {"event": self})
            self.upcoming_notification_1_sent = True
            self.save()
        else:
            user.send_email("events/upcoming_1", {"event": self})


class EventTodo(models.Model):

    """ Represents actions which need to be taken to prepare for an event. """

    event = models.ForeignKey(Event, related_name="todos")
    title = models.CharField(max_length=255)
    notes = models.TextField()
    # May be unassigned
    assigned_to = models.ForeignKey("auth.User", null=True,
                                    related_name="assigned_todos")
    # May be uncompleted
    completed_by = models.ForeignKey("auth.User", null=True,
                                     related_name="completed_todos")
    completed_at = models.DateTimeField(null=True)


class EventSolution(models.Model):

    """ A solution from a team at a dojo. """

    event = models.ForeignKey(Event, related_name="solutions")
    team_number = models.IntegerField(default=0)
    team_name = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    github_url = models.URLField()

    @property
    def name(self):
        """ Return the team name, or team number if there is none. """
        return self.team_name if self.team_name else \
            "Group %s" % self.team_number

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
    did_not_attend = models.NullBooleanField()
    group = models.IntegerField(null=True)
    votes = JSONField(null=True)

    @property
    def has_submitted_group_info(self):
        """ True if the member submitted their group information. """
        return self.did_not_attend is not None or self.group is not None

    def change_number(self, number):
        """ Change the number on the ticket. """
        if number == 0:
            return self.cancel()

        if not self.event.is_future:
            raise DojoFinishedError()

        if ((self.event.remaining_tickets + self.number) - number) < 0:
            # We've ran out of tickets
            raise NoTicketsError()

        if self.cancelled:
            raise TicketCancelledError()

        self.number = number
        self.save()
        self.user.send_email("events/edited_tickets", {"ticket": self})

    def cancel(self):
        """ Cancel the ticket. """
        if not self.event.is_future:
            raise DojoFinishedError()
        if not self.cancelled:
            self.cancelled = True
            self.cancelled_datetime = timezone.now()
            self.save()
            self.user.send_email("events/cancelled_tickets", {"ticket": self})

    def __unicode__(self):
        """ Return the . """
        return "%s's ticket to %s" % (self.user, self.event)
