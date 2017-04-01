"""General middleware."""
from django.utils.cache import patch_vary_headers


class VaryByHostMiddleware(object):

    """Different cache per hostname."""

    def process_response(self, request, response):
        """Add "host" to cache key."""
        patch_vary_headers(response, ('Host',))
        return response
