"""Members navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="members", name="Members")
def members_navigation_item(request, context):
    """Link to members category."""
    return render_to_string("members/navigation_items/members.html", context,
                            request=request)
