"""General middleware."""
from django.utils.cache import patch_vary_headers
from urlparse import urlsplit, urlunsplit
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from pages.configuration import ForceSSL


class VaryByHostMiddleware(object):

    """Different cache per hostname."""

    def process_response(self, request, response):
        """Add "host" to cache key."""
        patch_vary_headers(response, ('Host',))
        return response


class SSLifyMiddleware(object):

    """Force all requests to use HTTPs.

    If we get an HTTP request, we'll just force a redirect to HTTPs.

    This is modified from django-sslify
    """

    def process_request(self, request):
        """Force requests to use HTTPs."""
        # If the user has explicitly disabled SSLify, do nothing.
        if getattr(settings, 'SSLIFY_DISABLE', settings.DEBUG):
            return None

        if not ForceSSL().get():
            # Listen to configuration
            return None

        # If we get here, proceed as normal.
        if not request.is_secure():
            url = request.build_absolute_uri(request.get_full_path())
            url_split = urlsplit(url)
            scheme = 'https' if url_split.scheme == 'http' else\
                url_split.scheme
            ssl_port = getattr(settings, 'SSLIFY_PORT', 443)
            url_secure_split = (scheme, "%s:%d" % (
                url_split.hostname or '', ssl_port)) + url_split[2:]
            secure_url = urlunsplit(url_secure_split)

            return HttpResponsePermanentRedirect(secure_url)
