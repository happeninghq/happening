"""General models."""
from django.db import models
from happening import db
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site


class ConfigurationVariable(db.Model):

    """Configuration Variable saved in database."""

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=255)
    value = models.TextField()


Site.happening_site = property(
    lambda s: HappeningSite.objects.get_or_create(site=s)[0])


class HappeningSite(db.Model):

    """Add site configuration."""

    site = models.ForeignKey(Site)
