"""Group forms."""

from django import forms
from django.forms import ModelForm
from models import Group


class GroupGenerationForm(forms.Form):

    """Generate groups for an event."""

    clear_existing_groups = forms.BooleanField(required=False)
    only_group_checked_in = forms.BooleanField(required=False)
    number_of_groups = forms.IntegerField()


class GroupForm(ModelForm):

    """Form for creating/editing events."""

    team_name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    github_url = forms.CharField(required=False)

    class Meta:
        model = Group
        fields = ['team_name', 'description', 'github_url']
