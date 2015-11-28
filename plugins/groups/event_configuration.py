"""Group Event Configuration."""
from happening import configuration


class GroupCreation(configuration.ChoiceField):

    """Who is able to create groups."""

    default = 0

    choices = [
        (0, "Attendees cannot create groups"),
        (1, "Attendees can create groups after the event starts"),
        (2, "Attendees can create groups at any time"),
        (3, "Attendees can create groups if they are checked in"),
    ]


class GroupMovement(configuration.ChoiceField):

    """When are people able to move between groups."""

    default = 0

    choices = [
        (0, "Attendees cannot move groups"),
        (1, "Attendees can move groups after the event starts"),
        (2, "Attendees can move groups at any time"),
        (3, "Attendees can move groups if they are checked in"),
    ]


class GroupEditing(configuration.ChoiceField):

    """When are people able to edit groups."""

    default = 0

    choices = [
        (0, "Attendees cannot edit groups"),
        (1, "Attendees can edit groups after the event starts"),
        (2, "Attendees can edit groups at any time"),
        (3, "Attendees can edit groups if they are checked in"),
    ]


class GroupProperties(configuration.PropertiesField):

    """What properties should be provided for groups."""

    pass
