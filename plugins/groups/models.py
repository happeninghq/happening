"""Group models."""

from django.db import models
from events.models import Event, Ticket


class Group(models.Model):

    """A group at an event."""

    event = models.ForeignKey(Event, related_name="groups")
    team_number = models.IntegerField(default=0)
    # TODO: Make a lot of this information admin configurable
    team_name = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    github_url = models.URLField()

    @property
    def name(self):
        """Return the team name, or team number if there is none."""
        return self.team_name if self.team_name else \
            "Group %s" % self.team_number

    def __unicode__(self):
        """Return the title of this solution."""
        return "%s %s" % (self.event, self.team_name)

    def members(self):
        """List members of this group."""
        return [t.user for t in Ticket.objects.filter(
            event=self.event, group=self.team_number)]


class TicketInGroup(models.Model):

    """A ticket in a group."""

    group = models.ForeignKey(Group, related_name="tickets")
    ticket = models.ForeignKey(Ticket, related_name="groups")
