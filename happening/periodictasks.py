"""General period tasks."""
from periodically.decorators import daily
from django.core.files.storage import default_storage
from datetime import datetime, timedelta


@daily
def delete_old_temporary_media():
    """Delete temporary media older than 24 hours."""
    one_day_old = datetime.now() - timedelta(days=1)
    for f in default_storage.listdir("tmp"):
        modified_time = default_storage.modified_time("tmp/%s" % f)
        if modified_time < one_day_old:
            # At least 24 hours old
            print "Deleting", f
            default_storage.delete("tmp/%s" % f)
