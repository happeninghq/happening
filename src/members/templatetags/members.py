"""Template tags relating to members."""

from django import template
from members.utils import allow_new_users

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_allow_new_users(context):
    """Are new users allowed."""
    return allow_new_users(context['request'])
