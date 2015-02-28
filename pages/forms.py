""" Page forms. """

from django.forms import ModelForm
from models import Page


class PageForm(ModelForm):

    """ Form for creating/editing pages. """

    class Meta:
        model = Page
        fields = ['url', 'title', 'path', 'content']
