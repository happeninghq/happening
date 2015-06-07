"""Generate CSS according to settings."""
from django.core.management.base import BaseCommand
from happening.appearance import generate_css
from django.conf import settings
import os


class Command(BaseCommand):

    """Generate CSS according to settings."""

    help = 'Generate CSS according to settings.'

    def handle(self, *args, **options):
        """Generate CSS according to settings."""
        directory = "%s/css" % settings.MEDIA_ROOT
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open("%s/generated.css" % directory, "w+") as o:
            o.write(generate_css())
