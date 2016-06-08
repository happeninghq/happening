"""Page models."""
from django.db import models
from happening import db
from django_pgjson.fields import JsonField


class Page(db.Model):

    """A static page."""

    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    content = JsonField(default={"blockLists": [[], []], "blocks": []})
