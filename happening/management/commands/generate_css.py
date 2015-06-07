"""Generate CSS according to settings."""
from django.core.management.base import BaseCommand
from happening.appearance import generate_css


class Command(BaseCommand):

    """Generate CSS according to settings."""

    help = 'Generate CSS according to settings.'

    def handle(self, *args, **options):
        """Generate CSS according to settings."""
        with open("static/css/generated.css", "w+") as o:
            o.write(generate_css())
