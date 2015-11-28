"""Member Profile."""

from django.db import models
from happening import db
from django.conf import settings
from cached_property import threaded_cached_property
from django_gravatar.helpers import get_gravatar_url, has_gravatar
from django.contrib.auth.models import User
from happening.storage import media_path

# Ensure that every user has an associated profile
User.profile = threaded_cached_property(
    lambda u: Profile.objects.get_or_create(user=u)[0])


def get_user_name(user):
    """Get the full name if available, otherwise username."""
    if user.get_full_name():
        return user.get_full_name()
    return user.username
User.name = get_user_name


class Profile(db.Model):

    """Member Profile."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name="existing_profile")

    bio = models.TextField()
    photo = models.ImageField(null=True,
                              upload_to=media_path("profile_photos"))

    show_facebook_urls = models.BooleanField(default=False)
    show_github_urls = models.BooleanField(default=False)
    show_linkedin_urls = models.BooleanField(default=False)
    show_twitter_urls = models.BooleanField(default=False)
    show_google_urls = models.BooleanField(default=False)
    show_stackexchange_urls = models.BooleanField(default=False)

    def __unicode__(self):
        """Return the name of the user."""
        formatted_name = "%s %s" % (self.user.first_name, self.user.last_name)
        if len(formatted_name) > 1:
            return formatted_name
        return self.user.username

    def has_gravatar(self):
        """Return True if the user has a gravatar photo."""
        return has_gravatar(self.user.email)

    def photo_url(self):
        """Return the most appropriate profile photo URL for the user."""
        if self.photo:
            return "%s%s" % (settings.MEDIA_URL, self.photo)
        return get_gravatar_url(self.user.email, size=500, default='retro')

    def github_urls(self):
        """Return a list of the user's github URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="github")]

    def facebook_urls(self):
        """Return a list of the user's facebook URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="facebook")]

    def linkedin_urls(self):
        """Return a list of the user's linkedin URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="linkedin")]

    def twitter_urls(self):
        """Return a list of the user's twitter URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="twitter")]

    def google_urls(self):
        """Return a list of the user's google URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="google")]

    def stackexchange_urls(self):
        """Return a list of the user's stackexchange URLs."""
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="stackexchange")]


def close_account(user):
    """Close a user's account."""
    # Clear the profile
    p = user.profile
    p.bio = ""
    p.photo.delete()
    p._data = {}
    p.save()

    # Clear the user
    user.is_active = False
    closed_account_number = 1
    username = "Closed Account %s" % closed_account_number
    while len(User.objects.filter(username=username)) > 0:
        closed_account_number += 1
        username = "Closed Account %s" % closed_account_number
    user.username = username
    user.first_name = ""
    user.last_name = ""

    # Remove email addresses
    [e.delete() for e in user.emailaddress_set.all()]

    # Remove social accounts
    [e.delete() for e in user.socialaccount_set.all()]

    user.save()
User.close_account = close_account
