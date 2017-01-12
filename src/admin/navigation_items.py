"""Admin navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="admin", name="Admin")
def admin_navigation_item(request, context):
    """Link to admin category."""
    # If this user has access to any admin functions then it should display
    # otherwise it should return an empty string
    from admin.views import index
    if not index.has_permission(request.user):
        return ""
    return render_to_string("admin/navigation_items/admin.html", context,
                            request=request)
