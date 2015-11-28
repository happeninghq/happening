"""Default group form additions."""
from happening import configuration


class CustomProperties(configuration.CustomProperties):

    """The custom properties added on event creation."""

    configuration_variable =\
        "plugins.groups.event_configuration.GroupProperties"
    configuration_variable_instance = "event"
