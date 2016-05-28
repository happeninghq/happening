"""Group models."""

from django.db import models
from happening import db
from events.models import Event, Ticket
from .notifications import GroupLeftNotification
from .notifications import GroupJoinedNotification


class Group(db.Model):

    """A group at an event."""

    event = models.ForeignKey(Event, related_name="raw_groups")
    team_number = models.IntegerField(default=0)
    team_name = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)

    @property
    def name(self):
        """Return the team name, or team number if there is none."""
        return self.team_name if self.team_name else \
            "Group %s" % self.team_number

    def __str__(self):
        """Return the name of this group."""
        return self.name

    def is_editable_by(self, user):
        """True if the group is editable by the given user."""
        if user.is_superuser:
            # Is admin
            return True
        if user.is_authenticated():
            for ticket in user.tickets.filter(event=self.event):
                for group in ticket.groups.all():
                    if group.group == self:
                        # Is a group member
                        return True
        return False

    def members(self):
        """List members of this group."""
        return [t.ticket.user for t in self.tickets.all()]

    def remove_user(self, user):
        """Remove a user from the group."""
        ticket_in_group = self.tickets.filter(ticket__user=user).first()
        if ticket_in_group:
            ticket_in_group.delete()
            for member in self.members():
                GroupLeftNotification(
                    member,
                    event=self.event,
                    group_name=str(self),
                    user=user,
                    user_name=str(user),
                    user_photo_url=user.profile.photo_url()
                ).send()
            return True
        return False

    def add_user(self, user):
        """Add a user to the group."""
        ticket = user.tickets.filter(event=self.event, cancelled=False).first()
        if ticket:
            if ticket.groups.count() == 0:
                # No groups yet
                TicketInGroup(group=self, ticket=ticket).save()
                for member in self.members():
                    if not member == user:
                        GroupJoinedNotification(
                            member,
                            event=self.event,
                            group_name=str(self),
                            user=user,
                            user_name=str(user),
                            user_photo_url=user.profile.photo_url()
                        ).send()
                return True
        return False


class TicketInGroup(db.Model):

    """A ticket in a group."""

    group = models.ForeignKey(Group, related_name="tickets")
    ticket = models.ForeignKey(Ticket, related_name="groups")


def get_group(ticket):
    """Get the group this ticket belongs to, or None."""
    group = ticket.groups.first()
    if group:
        return group.group
    return None

Ticket.group = get_group


def get_groups(event):
    """Get groups for an event, ordered by team_number."""
    return event.raw_groups.all().order_by('team_number')

Event.groups = get_groups


def get_ungrouped_tickets(event):
    """Get ungrouped users attending an event."""
    return [t for t in event.tickets.all() if not t.groups.count() > 0 and
            not t.cancelled]

Event.ungrouped_tickets = get_ungrouped_tickets


def get_ungrouped_users(event):
    """Get ungrouped users attending an event."""
    return set([t.user for t in event.ungrouped_tickets()])

Event.ungrouped_users = get_ungrouped_users
