"""Group tags."""
from django import template

register = template.Library()


@register.filter
def can_edit_group(user, group):
    """Can the given user edit the given group."""
    return group.is_editable_by(user)
