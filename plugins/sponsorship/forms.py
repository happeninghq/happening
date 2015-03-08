""" Sponsorship forms. """

from django.forms import ModelForm
from models import Sponsor


class SponsorForm(ModelForm):

    """ Form for creating/editing sponsors. """

    class Meta:
        model = Sponsor
        fields = ['name', 'description', 'url', 'logo']
