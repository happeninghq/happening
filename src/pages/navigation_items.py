"""General navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="sign_in")
def sign_in_navigation_item(request):
    """Link to sign in/sign out."""
    return render_to_string("pages/navigation_items/sign_in.html",
                            request=request)
