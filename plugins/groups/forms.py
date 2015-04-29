"""Group forms."""

from django import forms


class GroupGenerationForm(forms.Form):

    """Generate groups for an event."""

    clear_existing_groups = forms.BooleanField(required=False)
    only_group_checked_in = forms.BooleanField(required=False)
    number_of_groups = forms.IntegerField()
