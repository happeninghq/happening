"""Member middleware."""
from members.models import TrackingLink


class TrackingLinkMiddleware(object):

    """If a code is specified in GET, add it to the session."""

    def process_request(self, request):
        """If a code is specified in GET, add it to the session."""
        if request.GET.get("_c"):
            c = request.GET.get("_c")
            tracking_link = TrackingLink.objects.filter(code=c).first()
            if tracking_link:
                for tag in tracking_link.tags.all():
                    if request.user.is_authenticated():
                        request.user.tags.add(tag)
                    else:
                        if 'tags' not in request.session:
                            request.session['tags'] = []
                        request.session['tags'].append(tag.tag)
        return None
