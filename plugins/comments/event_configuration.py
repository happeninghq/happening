"""Event Configuration."""
from happening import configuration
from happening import plugins


class CommentOnGroups(configuration.BooleanField):
    """Can members comment on groups."""

    @property
    def editable(self):
        """Only enable if the groups plugin is enabled."""
        return plugins.plugin_enabled("plugins.groups")
