"""General models."""
from django.db import models
from happening import db
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.signing import Signer
from django_pgjson.fields import JsonField
from happening.storage import media_path

signer = Signer()


Site.happening_site = property(
    lambda s: HappeningSite.objects.get_or_create(site=s)[0])


class HappeningSite(db.Model):

    """Add site configuration."""

    site = models.ForeignKey(Site)

    theme_settings = JsonField(default={})

    logo = models.ImageField(upload_to=media_path("site"), null=True)


class Follow(db.Model):

    """A user following a topic."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="following")

    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    role = models.CharField(max_length=255)

    is_subscribed = models.BooleanField(default=True)


def follow(user, obj, role, force=False):
    """A user follows an object.

    If force is not True, then people who have previously
    unsubscribed will not be re-subscribed.

    Force should be used in response to user action.
    """
    object_type = ContentType.objects.get_for_model(obj)

    follow = Follow.objects.filter(
        user=user,
        target_content_type=object_type,
        target_object_id=obj.pk,
        role=role).first()

    if not follow:
        follow = Follow(user=user,
                        target_content_type=object_type,
                        target_object_id=obj.pk,
                        role=role,
                        is_subscribed=True)
        follow.save()
    elif force:
        follow.is_subscribed = True
        follow.save()


def unfollow(user, obj, role):
    """A user unfollows an object."""
    object_type = ContentType.objects.get_for_model(obj)

    follow = Follow.objects.filter(
        user=user,
        target_content_type=object_type,
        target_object_id=obj.pk,
        role=role).first()

    if not follow:
        follow = Follow(user=user,
                        target_content_type=object_type,
                        target_object_id=obj.pk,
                        role=role,
                        is_subscribed=False)

    follow.is_subscribed = False
    follow.save()


def is_following(user, obj, role):
    """A user follows an object."""
    object_type = ContentType.objects.get_for_model(obj)
    follow = Follow.objects.filter(
        user=user,
        target_content_type=object_type,
        target_object_id=obj.pk,
        role=role).first()
    if not follow:
        return False
    return follow.is_subscribed


def follow_object_code(user, obj, role):
    """Generate a signed object code."""
    object_type = ContentType.objects.get_for_model(obj)

    return signer.sign("%s:%s:%s:%s:%s" % (object_type.app_label,
                                           object_type.model,
                                           obj.id,
                                           role,
                                           user.pk))

User.follow = follow
User.unfollow = unfollow
User.is_following = is_following
User.follow_object_code = follow_object_code
