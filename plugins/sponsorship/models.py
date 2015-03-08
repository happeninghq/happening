""" Sponsorship models. """
from django.db import models
from website.db import Model, Manager
from events.models import Event


class Sponsor(Model):

    """ A Sponsor. """

    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    logo = models.ImageField(upload_to="sponsors")

    def __unicode__(self):
        """ Return the sponsor's name. """
        return self.name


class EventSponsor(Model):

    """ A sponsor for an individual event. """

    sponsor = models.ForeignKey(Sponsor, related_name="event_sponsors")
    event = models.ForeignKey(Event, related_name="event_sponsors")


def get_event_sponsor(event):
    """ Get a single sponsor for an event. """
    if event.event_sponsors.count() == 0:
        return None
    return event.event_sponsors.all()[0].sponsor

Event.sponsor = get_event_sponsor
