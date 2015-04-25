"""Group models."""

from django.db import models
from events.models import Event, Ticket


class Group(models.Model):

    """A group at an event."""

    event = models.ForeignKey(Event, related_name="raw_groups")
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
        """Return the name of this group."""
        return self.name

    def members(self):
        """List members of this group."""
        return [t.ticket.user for t in self.tickets.all()]


class TicketInGroup(models.Model):

    """A ticket in a group."""

    group = models.ForeignKey(Group, related_name="tickets")
    ticket = models.ForeignKey(Ticket, related_name="groups")


def get_group(ticket):
    """Get the group this ticket belongs to, or None."""
    return ticket.groups.first()

Ticket.group = get_group


def get_groups(event):
    """Get groups for an event, ordered by team_number."""
    return event.raw_groups.all().order_by('team_number')

Event.groups = get_groups


def get_ungrouped_users(event):
    """Get ungrouped users attending an event."""
    return set(
        [t.user for t in event.tickets.all() if not t.groups.count() > 0 and
         not t.cancelled])

Event.ungrouped_users = get_ungrouped_users
