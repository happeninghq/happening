"""Period tasks related to emails."""

from periodically.decorators import every
from models import Backup
from django.core.management.commands import dumpdata, flush, loaddata
from django.db import DEFAULT_DB_ALIAS
import zipfile
import StringIO
from happening.utils import capturing
from happening.storage import storage
from django.core.files import File
from datetime import datetime
import sys
import os
import shutil


@every(seconds=10)
def backup():
    """Complete any scheduled backups."""
    for backup in Backup.objects.all().filter(
            restore=False, complete=False):
        backup.started = True
        backup.save()
        with capturing() as output:
            dumpdata.Command().handle(
                format='json',
                database=DEFAULT_DB_ALIAS,
                use_natural_foreign_keys=True,
                exclude=['admin.backup',
                         'contenttypes.contenttype',
                         'sessions.session',
                         'periodically.executionrecord',
                         'auth.permission'])
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
        zf.writestr("backup/data.json", output[0])

        def write_to_zip(base_path, directory):
            directories, files = storage.listdir(directory)
            for d in directories:
                if not d == 'backups':
                    # We don't backup existing backups
                    write_to_zip(base_path + d + "/", directory + d + "/")
            for f in files:
                if f != '':
                    # For some reason we sometimes get a blank filename
                    ff = storage.open(directory + f)
                    zf.writestr(base_path + f, ff.read())

        write_to_zip("backup/media/", "")
        zf.close()

        f = File(s)
        backup.zip_file.save("backup.zip", f)
        backup.complete = True
        backup.complete_time = datetime.now()
        backup.save()


@every(seconds=10)
def restore():
    """Complete any scheduled restore."""
    for backup in Backup.objects.all().filter(
            restore=True):

        zf = zipfile.ZipFile(backup.zip_file.path, 'r')
        zf.extractall(members=[x for x in zf.namelist()
                               if x.startswith("backup/")])
        zf.close()

        # First flush the database
        flush.Command().handle(
            noinput=True,
            database=DEFAULT_DB_ALIAS,
            # We can do set this to false and add
            # the content types etc if there are any problems:
            load_initial_data=True
        )

        # Delete all media
        def delete_dir(directory):
            directories, files = storage.listdir(directory)
            for d in directories:
                delete_dir(directory + d + "/")
            for f in files:
                storage.delete(directory + f)
        delete_dir("")

        # ./manage loaddata
        loaddata.Command().handle(
            'backup/data.json',
            database=DEFAULT_DB_ALIAS,
            ignore=True
        )
        # Restore media
        for dirname, dirnames, filenames in os.walk("backup/media"):
            for filename in filenames:
                f = os.path.join(dirname, filename)[len("backup/media/"):]
                with open(os.path.join(dirname, filename)) as ff:
                    storage.save(f, ff)

        # Remove the backup directory
        shutil.rmtree('backup')

        # We need to quit as we have removed the task and the backup
        sys.exit(0)
