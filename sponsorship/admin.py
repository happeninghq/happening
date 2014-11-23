""" Sponsorship administration. """

from django.contrib import admin
from models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):

    """ Sponsor admin configuration. """

    pass
