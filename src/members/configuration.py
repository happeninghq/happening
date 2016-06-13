"""Members configuration."""
from happening import configuration


class ProfileProperties(configuration.PropertiesField):

    """The custom properties added to member profiles."""

    category = "Members"

    default = [
        # TODO: After name + bio are moved to use properties, put them here
    ]
