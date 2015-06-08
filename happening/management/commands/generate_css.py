"""Generate CSS according to settings."""
from django.core.management.base import BaseCommand
from happening.appearance import generate_css
from django.core.files.storage import default_storage
from django.core.files import File


class Command(BaseCommand):

    """Generate CSS according to settings."""

    help = 'Generate CSS according to settings.'

    def handle(self, *args, **options):
        """Generate CSS according to settings."""
        # if not c.
        if not default_storage.exists("css/generated.css"):
            # We'll create the file with rubbish in it
            # - to create the structure
            default_storage.save("css/generated.css",
                                 File(open("README.md")),
                                 content_type="text/css")
        with default_storage.open("css/generated.css", "w+") as o:
            o.write(generate_css())
