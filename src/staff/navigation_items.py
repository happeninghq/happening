"""Staff navigation items."""

from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="staff", name="Staff")
def staff_navigation_item(request, context):
    """Link to staff category."""
    return render_to_string("staff/navigation_items/staff.html", context,
                            request=request)
