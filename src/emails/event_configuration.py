"""Event Configuration."""
from happening import configuration


class Emails(configuration.EmailsField):

    """Emails to create with this event."""

    editable = False
