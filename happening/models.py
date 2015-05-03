"""General models."""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ConfigurationVariable(models.Model):

    """Configuration Variable saved in database."""

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=255)
    value = models.TextField()
