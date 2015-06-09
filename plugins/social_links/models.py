"""Social link models."""
from django.db import models
from happening import db


class SocialLink(db.Model):

    """A Social Link."""

    provider = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
