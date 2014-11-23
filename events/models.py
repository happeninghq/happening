""" Event models. """
from django.db import models
from sponsorship.models import Sponsor
from django.utils import timezone


class EventManager(models.Manager):

    """ Custom Event Manager, to add site-wide functionality. """

    def latest_event(self):
        next_event = self.filter(datetime__gte=timezone.now()).order_by("datetime").first()
        if next_event:
            return next_event
        return self.order_by("-datetime").first()



class Event(models.Model):

    """ A code dojo event. """

    objects = EventManager()

    datetime = models.DateTimeField(primary_key=True)

    # This can be null if this event isn't sponsored
    sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

    eventbrite_url = models.URLField()

    # If completed, this information will be used on the "info" page
    challenge_language = models.CharField(max_length=200, blank=True,
                                          null=True)
    challenge_title = models.CharField(max_length=200, blank=True, null=True)

    challenge_text = models.TextField(blank=True, null=True)
    solution_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="event_images", blank=True, null=True)

    def is_future(self):
        """ Return True if this event is in the future. False otherwise. """
        return self.datetime > timezone.now()

    def challenge(self):
        if self.challenge_language and self.challenge_title:
            return "%s %s" % (self.challenge_language, self.challenge_title)
        elif self.challenge_title:
            return self.challenge_title
        elif self.challenge_language:
            return self.challenge_language
        return None

    def heading(self):
        s = self.__unicode__()
        if self.challenge():
            s += " (%s)" % self.challenge()
        return "%s (%s)" % (self.__unicode__(), self.challenge()) if\
            self.challenge() else self.__unicode__()

    def month_year(self):
        return self.datetime.strftime("%B %Y")

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