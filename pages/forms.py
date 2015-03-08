""" Page forms. """

from django import forms
from django.forms import ModelForm
from models import Page


class PageForm(ModelForm):

    """ Form for creating/editing pages. """

    path = forms.CharField(required=False)

    class Meta:
        model = Page
        fields = ['url', 'title', 'path', 'content']
