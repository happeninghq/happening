"""Comment models."""
from django.db import models
from happening import db
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from events.models import Event


class Comment(db.Model):

    """A comment."""

    parent_content_type = models.ForeignKey(ContentType)
    parent_object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_content_type', 'parent_object_id')

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


def get_comments_for_object(obj):
    """Get comments for a given object."""
    object_type = ContentType.objects.get_for_model(obj)

    comments = Comment.objects.filter(
        parent_content_type=object_type,
        parent_object_id=obj.pk).order_by('-created_at')
    return comments

Event.comments = get_comments_for_object
