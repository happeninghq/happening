"""Special configuration for AllAuth."""

from allauth.account.adapter import DefaultAccountAdapter
from .utils import allow_new_users


class AccountAdapter(DefaultAccountAdapter):

    """Account Adapter which has a special case for first login."""

    def get_login_redirect_url(self, request):
        """Get the redirect URL for the request."""
        threshold = 90  # seconds

        time_passed = (request.user.last_login - request.user.date_joined)
        if time_passed.seconds < threshold:
            return '/member/%s/edit' % request.user.pk
        else:
            return '/'

    def is_open_for_signup(self, request):
        """
        Check whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return allow_new_users(request)
