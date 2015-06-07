"""General period tasks."""
from periodically.decorators import daily
import time
import os
from django.conf import settings


@daily
def delete_old_temporary_media():
    """Delete temporary media older than 24 hours."""
    now = time.time()
    path = '%s/tmp' % settings.MEDIA_ROOT
    for f in os.listdir(path):
        if os.stat(os.path.join(path, f)).st_mtime < now - 86400:
            # At least 24 hours old
            print "Deleting", f
            os.remove(os.path.join(path, f))
