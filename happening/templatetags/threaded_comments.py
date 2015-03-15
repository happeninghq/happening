"""Template tags relating to threaded comments."""

from django import template
from django_comments.models import Comment

register = template.Library()


@register.filter()
def reverse_comments(comment_list, object):
    """Reverse the comment order if root comment."""
    if isinstance(object, Comment):
        return comment_list
    comment_list.reverse()
    return comment_list


@register.filter()
def is_root_comment(comment):
    """True if this a root comment."""
    if isinstance(comment.content_object, Comment):
        return False
    return True
