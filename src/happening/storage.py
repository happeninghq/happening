"""Allow for central modification of storage."""
from django.core.files.storage import default_storage

storage = default_storage


def inner():
    """Temp. Will be removed."""
    return ""


def media_path(path):
    """Get the path to upload files to.

    This is to be used with upload_to.
    """
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ('makemigrations', 'migrate'):
        return None  # Hide ourselves from Django migrations

    def inner(instance, filename):
        ext = filename.rsplit(".", 1)[-1]
        # TODO: this loses the original filename
        filename = filename.rsplit("/", 1)[-1].rsplit("_", 1)[0]
        if "." not in filename:
            filename += "." + ext
        return '/'.join([path, filename])
    return inner
