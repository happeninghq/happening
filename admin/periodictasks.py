"""Period tasks related to emails."""

from periodically.decorators import every
from models import Backup
from django.core.management.commands import dumpdata
from django.db import DEFAULT_DB_ALIAS
import zipfile
import StringIO
from happening.utils import capturing
from happening.storage import storage
from django.core.files import File
from datetime import datetime


@every(minutes=10)
def backup():
    """Complete any scheduled backups."""
    for backup in Backup.objects.all().filter(
            complete=False):
        backup.started = True
        backup.save()
        with capturing() as output:
            dumpdata.Command().handle(
                format='json',
                database=DEFAULT_DB_ALIAS,
                use_natural_foreign_keys=True,
                exclude=['admin.backup'])
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
        zf.writestr("backup/data.json", str(output))

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
