"""Generate CSS according to settings."""
from django.core.management.base import BaseCommand
from happening.appearance import generate_css
import os


class Command(BaseCommand):

    """Generate CSS according to settings."""

    help = 'Generate CSS according to settings.'

    def handle(self, *args, **options):
        """Generate CSS according to settings."""
        if not os.path.exists("static/css"):
            os.makedirs("static/css")
        with open("static/css/generated.css", "w+") as o:
            o.write(generate_css())
