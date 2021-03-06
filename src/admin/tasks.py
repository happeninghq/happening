"""Period tasks related to emails."""

from happening.tasks import task
from .models import Backup
from django.core.management.commands import dumpdata  # , flush, loaddata
from django.db import DEFAULT_DB_ALIAS
import zipfile
import io
from happening.utils import capturing
from happening.storage import storage
from django.core.files import File
from datetime import datetime
# import os
# import shutil


@task
def backup():
    """Create a backup."""
    backup = Backup(started=True)
    backup.save()

    with capturing() as output:
        dumpdata.Command().handle(
            format='json',
            database=DEFAULT_DB_ALIAS,
            use_natural_foreign_keys=True,
            exclude=['admin.backup',
                     'contenttypes.contenttype',
                     'sessions.session',
                     'auth.permission'])
    s = io.BytesIO()
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
    backup.zip_file.save("backup.bak", f)
    backup.complete = True
    backup.complete_time = datetime.now()
    backup.save()


# @task
# def restore(backup_id):
    # """Restore from backup."""
    # backup = Backup.objects.get(pk=backup_id)

    # # with storage.open(backup.zip_file.name, 'r') as o:
    # with zipfile.ZipFile(backup.zip_file, 'r') as zf:
    #     zf.extractall(members=[x for x in zf.namelist()
    #                            if x.startswith("backup/")])

    # flush_database()

    # # # Delete all media
    # def delete_dir(directory):
    #     directories, files = storage.listdir(directory)
    #     for d in directories:
    #         delete_dir(directory + d + "/")
    #     for f in files:
    #         storage.delete(directory + f)
    # delete_dir("")

    # # # ./manage loaddata
    # # loaddata.Command().handle(
    # #     'backup/data.json',
    # #     database=DEFAULT_DB_ALIAS,
    # #     ignore=True
    # # )
    # # # Restore media
    # for dirname, dirnames, filenames in os.walk("backup/media"):
    #     for filename in filenames:
    #         f = os.path.join(dirname, filename)[len("backup/media/"):]
    #         with open(os.path.join(dirname, filename)) as ff:
    #             storage.save(f, ff)

    # # Remove the backup directory
    # shutil.rmtree('backup')
