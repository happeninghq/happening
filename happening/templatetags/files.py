"""File management."""
from django import template
import os

register = template.Library()


@register.filter
def filename(file):
    """Get just the filename from a file."""
    return os.path.basename(file.name)
