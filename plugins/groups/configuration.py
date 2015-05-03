"""Group Event Configuration."""
from happening import configuration


class GroupCreation(configuration.ChoiceField):

    """Who is able to create groups."""

    default = 0

    choices = [
        (0, "Members cannot create groups"),
        (1, "Members can create groups after the event starts"),
        (2, "Members can create groups at any time"),
    ]
