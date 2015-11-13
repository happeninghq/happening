"""Social Links configuration."""
from happening import configuration


class SocialLinksTitle(configuration.CharField):
    """The message shown alongside social links."""

    default = "Follow us"
