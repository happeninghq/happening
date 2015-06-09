"""Social links template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from models import SocialLink


@plugin_block("happening.footer")
def social_links(request):
    """Add social links links to footer."""
    if SocialLink.objects.count() == 0:
        # No socia links, don't show it
        return ""

    return render_to_string(
        "social_links/blocks/happening/footer.html",
        {"social_links": SocialLink.objects.all()})
