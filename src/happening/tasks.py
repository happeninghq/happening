"""General period tasks."""
from happening.storage import storage
from datetime import timedelta
from django.utils import timezone
from celery.decorators import periodic_task as celery_periodic_task
import inspect
from happening.plugins import plugin_enabled


def periodic_task(*o_args, **o_kwargs):
    """Schedule a task to run periodically."""
    def periodic_task_inner(f):
        plugin_id = inspect.getmodule(f).__name__[:-len(".tasks")]

        def periodic_task_inner_inner(*args, **kwargs):
            # First check if this plugin is enabled, if not return
            if not plugin_enabled(plugin_id):
                return False
            return f()
        if 'name' not in o_kwargs:
            o_kwargs['name'] = f.__name__
        o_kwargs['name'] = '%s.tasks.%s' % (plugin_id, o_kwargs['name'])
        return celery_periodic_task(*o_args, **o_kwargs)(
            periodic_task_inner_inner)
    return periodic_task_inner


@periodic_task(run_every=timedelta(days=1))
def delete_old_temporary_media():
    """Delete temporary media older than 24 hours."""
    one_day_old = timezone.now() - timedelta(days=1)
    for f in storage.listdir("tmp"):
        modified_time = storage.modified_time("tmp/%s" % f)
        if modified_time < one_day_old:
            # At least 24 hours old
            storage.delete("tmp/%s" % f)
