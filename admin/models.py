"""Admin models."""
from django.db import models


class PluginSetting(models.Model):

    """Setting if a plugin is enabled or disabled for the current site."""

    plugin_name = models.CharField(max_length=255, primary_key=True)
    enabled = models.BooleanField(default=False)
