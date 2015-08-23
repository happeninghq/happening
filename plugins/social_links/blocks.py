"""Social links template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from models import SocialLink


@plugin_block("index.secondary_content")
def social_links(request):
    """Add social links links to index."""
    if SocialLink.objects.count() == 0:
        # No social links, don't show it
        return ""

    return render_to_string(
        "social_links/blocks/index/secondary_content.html",
        {"social_links": SocialLink.objects.all()})
