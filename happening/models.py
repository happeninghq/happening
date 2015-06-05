"""General models."""
from django.db import models
from happening import db
from django.contrib.sites.models import Site


Site.happening_site = property(
    lambda s: HappeningSite.objects.get_or_create(site=s)[0])


class HappeningSite(db.Model):

    """Add site configuration."""

    site = models.ForeignKey(Site)

    # Theme settings
    theme_colour = models.CharField(max_length=7, default="#65afdc")
    primary_colour = models.CharField(max_length=7, default="#008CBA")
