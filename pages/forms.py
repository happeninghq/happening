"""Page forms."""

from django.forms import ModelForm
from happening.forms import MarkdownField
from models import Page


class PageForm(ModelForm):

    """Form for creating/editing pages."""

    content = MarkdownField()

    class Meta:
        model = Page
        fields = ['url', 'title', 'content']
