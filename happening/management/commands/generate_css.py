"""Generate CSS according to settings."""
from django.core.management.base import BaseCommand
from happening.appearance import generate_css
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.files import File


class Command(BaseCommand):

    """Generate CSS according to settings."""

    help = 'Generate CSS according to settings.'

    def handle(self, *args, **options):
        """Generate CSS according to settings."""
        directory = "%s/css" % settings.MEDIA_ROOT
        c = get_storage_class()()
        # if not c.
        if not c.exists("%s/generated.css" % directory):
            # We'll create the file with rubbish in it
            # - to create the structure
            c.save("%s/generated.css" % directory, File(open("README.md")))
        with c.open("%s/generated.css" % directory, "w+") as o:
            o.write(generate_css())
