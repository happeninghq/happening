"""Pages configuration."""
from happening import configuration


class NameOfEvents(configuration.CharField):

    """The term used to refer to an event, e.g. "match", "rally"."""

    default = "event"


class GoogleAnalyticsCode(configuration.CharField):

    """If you use Google analytics. Put the code here."""

    default = ""


class SiteTitle(configuration.CharField):

    """The title of the website."""

    default = "Happening Demo Site"


class ProfileProperties(configuration.PropertiesField):

    """The properties available for member profiles."""

    default = [
        # TODO: After name + bio are moved to use properties, put them here
    ]
