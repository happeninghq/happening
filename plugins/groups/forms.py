"""Group forms."""

from django import forms
from django.forms import ModelForm
from .models import Group
from happening.forms import MarkdownWidget


class GroupGenerationForm(forms.Form):

    """Generate groups for an event."""

    clear_existing_groups = forms.BooleanField(required=False)
    only_group_checked_in = forms.BooleanField(required=False)
    number_of_groups = forms.IntegerField()


class GroupForm(ModelForm):

    """Form for creating/editing events."""

    team_name = forms.CharField(required=False)
    description = forms.CharField(widget=MarkdownWidget(), required=False)

    class Meta:
        model = Group
        fields = ['team_name', 'description']


class ChangeGroupForm(forms.Form):

    """Change an attendee's group."""

    def __init__(self, *args, **kwargs):
        """Change an attendee's group."""
        groups = kwargs.pop("groups")
        super(ChangeGroupForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ChoiceField(
            choices=[(None, "None")] +
                    [(o.id, str(o)) for o in groups])

    def clean_group(self):
        """Turn the group ID into a Group."""
        data = self.cleaned_data['group']
        if not data:
            return data
        return Group.objects.get(pk=data)
