""" Event administration. """

from django.contrib import admin
from models import Event, EventSolution


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    """ Admin configuration for Events. """

    pass


@admin.register(EventSolution)
class EventSolutionAdmin(admin.ModelAdmin):

    """ Admin configuration for solutions. """

    pass
