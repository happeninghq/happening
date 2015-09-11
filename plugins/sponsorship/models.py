"""Sponsorship models."""
from django.db import models
from happening import db
from events.models import Event
from happening.storage import media_path


class Sponsor(db.Model):

    """A Sponsor."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    logo = models.ImageField(upload_to=media_path("sponsors"))

    def __unicode__(self):
        """Return the sponsor's name."""
        return self.name


class EventSponsor(db.Model):

    """A sponsor for an individual event."""

    sponsor = models.ForeignKey(Sponsor, related_name="event_sponsors")
    event = models.ForeignKey(Event, related_name="event_sponsors")


class SponsorTier(db.Model):

    """A tier for a sponsor to sponsor the entire community."""

    name = models.CharField(max_length=200)

    def __unicode__(self):
        """Return tier name."""
        return self.name


class CommunitySponsorship(db.Model):

    """An instance of a sponsor sponsoring the community."""

    sponsor = models.ForeignKey(Sponsor, related_name="community_sponsorships")
    tier = models.ForeignKey(SponsorTier,
                             related_name="community_sponsorships")


def get_event_sponsor(event):
    """Get a single sponsor for an event."""
    if event.event_sponsors.count() == 0:
        return None
    return event.event_sponsors.all()[0].sponsor

Event.sponsor = get_event_sponsor
