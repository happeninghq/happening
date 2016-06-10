from git import Repo
from django.core.management.base import BaseCommand
import shutil
import importlib
import os


class Command(BaseCommand):
    """Install a happening plugin."""

    help = 'Install a happening plugin'

    def add_arguments(self, parser):  # NOQA
        parser.add_argument('git_url', nargs='+', type=str)
        parser.add_argument(
            '--dev',
            action='store_true',
            dest='dev',
            default=False,
            help='Symlink instead of cloning',
        )

    def handle(self, *args, **options):  # NOQA
        git_url = options['git_url'][0]
        if options.get('dev'):
            print('Linking plugin to %s' % git_url)
            if not git_url.startswith('file://'):
                print('Dev paths must begin with file://')
            os.symlink(git_url[7:], 'tmp_plugin_install')
            src = importlib.import_module("tmp_plugin_install.src")
            plugin = src.Plugin

            plugin_name = plugin.name
            plugin_dir = plugin_name.lower()
            print('Linking %s to plugins directory' % plugin_name)
            os.symlink("%s/src" % git_url[7:], 'plugins/%s' % plugin_dir)

            os.unlink('tmp_plugin_install')

        else:
            print("Loading plugin from %s" % git_url)
            Repo.clone_from(git_url, "tmp_plugin_install")
            src = importlib.import_module("tmp_plugin_install.src")
            plugin = src.Plugin

            plugin_name = plugin.name
            plugin_dir = plugin_name.lower()
            print('Copying %s to plugins directory' % plugin_name)
            shutil.move('tmp_plugin_install/src', 'plugins/%s' % plugin_dir)
            shutil.rmtree('tmp_plugin_install')
            print("%s is now installed" % plugin_name)
