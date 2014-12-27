""" Special configuration for AllAuth. """

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    """ Account Adapter which has a special case for first login. """

    def get_login_redirect_url(self, request):
        """ Get the redirect URL for the request. """
        threshold = 90  # seconds

        time_passed = (request.user.last_login - request.user.date_joined)
        if time_passed.seconds < threshold:
            return '/member/%s/edit' % request.user.pk
        else:
            return '/'
