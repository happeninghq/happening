""" Member Profile. """

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cached_property import threaded_cached_property
from django_gravatar.helpers import get_gravatar_url, has_gravatar
from templated_email import send_templated_mail

# Ensure that every user has an associated profile
User.profile = threaded_cached_property(
    lambda u: Profile.objects.get_or_create(user=u)[0])


def send_email_to_user(user, template, context):
    """ Send an email to a user. """
    if "user" not in context:
        context["user"] = user

    send_templated_mail(
        template_name=template,
        from_email='Southampton Code Dojo <admin@southamptoncodedojo.com>',
        recipient_list=[user.email],
        context=context,
    )
User.send_email = send_email_to_user


class Profile(models.Model):

    """ Member Profile. """

    user = models.OneToOneField("auth.User", related_name="existing_profile")

    bio = models.TextField()
    photo = models.ImageField(null=True, upload_to="media/profile_photos")

    def __unicode__(self):
        """ Return the name of the user. """
        if self.user.first_name is not None or self.user.last_name is not None:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        return self.user.username

    def has_gravatar(self):
        """ Return True if the user has a gravatar photo. """
        return has_gravatar(self.user.email)

    def photo_url(self):
        """ Return the most appropriate profile photo URL for the user. """
        if self.photo:
            return "%s%s" % (settings.MEDIA_URL, self.photo)
        elif self.has_gravatar():
            return get_gravatar_url(self.user.email, size=500)
        return "%simg/dojo-logo.png" % settings.STATIC_URL

    def github_url(self):
        """ Return the user's github URL, or None if they do not have one. """
        for x in self.user.socialaccount_set.filter(provider="github"):
            return x.get_profile_url()
        return None
