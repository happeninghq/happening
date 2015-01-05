""" Member Profile. """

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cached_property import threaded_cached_property
from django_gravatar.helpers import get_gravatar_url, has_gravatar
from templated_email import send_templated_mail
# from notifications import send_notification_to_user

# Ensure that every user has an associated profile
User.profile = threaded_cached_property(
    lambda u: Profile.objects.get_or_create(user=u)[0])

# User.send_notification = send_notification_to_user


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

    show_facebook_urls = models.BooleanField(default=False)
    show_github_urls = models.BooleanField(default=False)
    show_linkedin_urls = models.BooleanField(default=False)
    show_twitter_urls = models.BooleanField(default=False)
    show_google_urls = models.BooleanField(default=False)
    show_stackexchange_urls = models.BooleanField(default=False)

    def __unicode__(self):
        """ Return the name of the user. """
        formatted_name = "%s %s" % (self.user.first_name, self.user.last_name)
        if len(formatted_name) > 1:
            return formatted_name
        return self.user.username

    def has_gravatar(self):
        """ Return True if the user has a gravatar photo. """
        return has_gravatar(self.user.email)

    def photo_url(self):
        """ Return the most appropriate profile photo URL for the user. """
        if self.photo:
            return "%s%s" % (settings.MEDIA_URL, self.photo)
        return get_gravatar_url(self.user.email, size=500, default='retro')

    def github_urls(self):
        """ Return a list of the user's github URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="github")]

    def facebook_urls(self):
        """ Return a list of the user's facebook URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="facebook")]

    def linkedin_urls(self):
        """ Return a list of the user's linkedin URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="linkedin")]

    def twitter_urls(self):
        """ Return a list of the user's twitter URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="twitter")]

    def google_urls(self):
        """ Return a list of the user's google URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="google")]

    def stackexchange_urls(self):
        """ Return a list of the user's stackexchange URLs. """
        return [x.get_profile_url() for x in
                self.user.socialaccount_set.filter(provider="stackexchange")]
