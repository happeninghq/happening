"""Page models."""
from django.db import models
from happening import db


class Page(db.Model):

    """A static page."""

    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
