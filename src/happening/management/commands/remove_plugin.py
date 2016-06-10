from django.core.management.base import BaseCommand
import shutil
import os


class Command(BaseCommand):
    """Uninstall a happening plugin."""

    help = 'Uninstall a happening plugin'

    def add_arguments(self, parser):  # NOQA
        parser.add_argument('plugin_name', nargs='+', type=str)

    def handle(self, *args, **options):  # NOQA
        plugin_name = options['plugin_name'][0]
        print("Removing %s from plugins directory" % plugin_name)
        if os.path.islink('plugins/%s' % plugin_name):
            os.unlink('plugins/%s' % plugin_name)
        else:
            shutil.rmtree('plugins/%s' % plugin_name)
        print("%s is now uninstalled" % plugin_name)
