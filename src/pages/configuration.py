"""Pages configuration."""
from happening import configuration
from events.models import Event


class NameOfEvents(configuration.CharField):

    """The term used to refer to an event, e.g. "match", "rally"."""

    default = "event"
    category = "Display"


class GoogleAnalyticsCode(configuration.CharField):

    """If you use Google analytics. Put the code here."""

    default = ""
    can_be_disabled = True
    default_enabled = False
    category = "Analytics"


class SiteTitle(configuration.CharField):

    """The title of the website."""

    default = "Happening Demo Site"
    category = "Display"


class ForceSSL(configuration.BooleanField):

    """Should SSL be forced."""

    default = False
    category = "Security"


class PrimaryEvent(configuration.ChoiceField):

    """If one is selected, the primary event will replace index."""

    can_be_disabled = True
    default_enabled = False
    category = "Display"

    def __init__(self, *args, **kwargs):
        """Setup choices."""
        super(PrimaryEvent, self).__init__(*args, **kwargs)
        self.choices = [
            (str(e.pk), e.title) for e in Event.objects.all()]
