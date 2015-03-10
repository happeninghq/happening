""" General site-wide models. """

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from happening.db import Manager as SiteManager


class Manager(UserManager, SiteManager):

    """ User manager which restricts to the current site. """

    pass


class User(AbstractBaseUser, PermissionsMixin):

    """ A copy of the AbstractUser with site added and unique with username.

    This can't extend AbstractUser as it needs to replace username field.
    """

    site = models.ForeignKey(Site)
    username = models.CharField(
        _('username'), max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = Manager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = (("site", "username"),)

    def get_full_name(self):
        """ Return the first_name plus the last_name. """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Return the short name for the user. """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User. """
        send_mail(subject, message, from_email, [self.email], **kwargs)
