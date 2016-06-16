"""General period tasks."""
from happening.storage import storage
from datetime import timedelta
from django.utils import timezone
from celery.decorators import periodic_task


@periodic_task(run_every=timedelta(days=1))
def delete_old_temporary_media():
    """Delete temporary media older than 24 hours."""
    one_day_old = timezone.now() - timedelta(days=1)
    for f in storage.listdir("tmp"):
        modified_time = storage.modified_time("tmp/%s" % f)
        if modified_time < one_day_old:
            # At least 24 hours old
            storage.delete("tmp/%s" % f)
