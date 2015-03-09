""" Custom happening auth backend. """
from django.contrib.sites.models import Site
from allauth.account.auth_backends import AuthenticationBackend


class SiteBackend(AuthenticationBackend):

    """ A backend which ensures the user belongs to the correct site. """

    def authenticate(self, **credentials):
        """ Ensure we only authenticate users for the current site. """
        user_or_none = super(SiteBackend, self).authenticate(**credentials)
        if user_or_none and\
                user_or_none.profile.site != Site.objects.get_current():
            user_or_none = None
        return user_or_none

    def get_user(self, user_id):
        """ Ensure we only get users for the current site. """
        user_or_none = super(SiteBackend, self).get_user(user_id)
        if user_or_none and\
                user_or_none.profile.site != Site.objects.get_current():
            user_or_none = None
        return user_or_none
