"""Admin models."""
from django.db import models
from happening import db
from happening.storage import media_path


class PluginSetting(db.Model):

    """Setting if a plugin is enabled or disabled for the current site."""

    plugin_name = models.CharField(max_length=255, primary_key=True)
    enabled = models.BooleanField(default=False)


class Backup(db.Model):

    """A backup which needs to be generated/restored."""

    # If this is true then we're restoring rather than generating
    restore = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    complete_time = models.DateTimeField(null=True)
    zip_file = models.FileField(null=True,
                                upload_to=media_path("backups"))
