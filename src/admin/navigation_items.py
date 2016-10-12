"""Admin navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="admin")
def admin_navigation_item(request, context):
    """Link to admin category."""
    return render_to_string("admin/navigation_items/admin.html", context,
                            request=request)
