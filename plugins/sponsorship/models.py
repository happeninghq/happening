""" Sponsorship models. """
from django.db import models
from events.models import Event


class Sponsor(models.Model):

    """ A Sponsor. """

    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    logo = models.ImageField(upload_to="sponsors")

    def __unicode__(self):
        """ Return the sponsor's name. """
        return self.name


class EventSponsor(models.Model):

    """ A sponsor for an individual event. """

    sponsor = models.ForeignKey(Sponsor, related_name="event_sponsors")
    event = models.ForeignKey(Event, related_name="event_sponsors")
