"""Members configuration."""
from happening import configuration


class MembersListVisibility(configuration.ChoiceField):

    """Who should be able to view members lists."""

    category = "Members"

    default = "All"

    choices = [
        ("staff", "Staff"),
        ("members", "Members"),
        ("all", "All"),
    ]


class ProfileProperties(configuration.PropertiesField):

    """The custom properties added to member profiles."""

    category = "Members"

    default = [
        # TODO: After name + bio are moved to use properties, put them here
    ]
