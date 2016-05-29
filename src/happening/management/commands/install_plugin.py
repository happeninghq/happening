from git import Repo
from django.core.management.base import BaseCommand
import shutil
import importlib


class Command(BaseCommand):
    """Install a happening plugin."""

    help = 'Install a happening plugin'

    def add_arguments(self, parser):  # NOQA
        parser.add_argument('git_url', nargs='+', type=str)

    def handle(self, *args, **options):  # NOQA
        git_url = options['git_url'][0]
        print("Loading plugin from %s" % git_url)
        Repo.clone_from(git_url, "tmp_plugin_install")
        src = importlib.import_module("tmp_plugin_install.src")
        plugin = src.Plugin

        plugin_name = plugin.name
        plugin_dir = plugin_name.lower()
        print("Copying %s to plugins directory" % plugin_name)
        shutil.move('tmp_plugin_install/src', 'plugins/%s' % plugin_dir)
        shutil.rmtree('tmp_plugin_install')
        print("%s is now installed" % plugin_name)
