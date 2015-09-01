"""Comment forms."""
from django import forms
from models import Comment
from happening.forms import MarkdownField


class CommentForm(forms.ModelForm):

    """Form for creating comments."""

    content = MarkdownField(label="Post Comment")

    class Meta:
        model = Comment
        fields = ['content']
