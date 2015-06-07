"""General Happening views."""
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse
from happening.utils import format_bytes
from uuid import uuid4
from PIL import Image
from django.core.files.storage import get_storage_class


@require_POST
def file_upload(request):
    """Handle an ajax file upload."""
    c = get_storage_class()()
    uuid = uuid4().hex
    filename = request.FILES['files[]'].name
    filepath = '%s/tmp/%s_%s' % (settings.MEDIA_ROOT, uuid, filename)
    with c.open(filepath, 'wb+') as destination:
        for chunk in request.FILES['files[]'].chunks():
            destination.write(chunk)

    filesize = c.size(filepath)

    request.FILES['files[]'].seek(0)
    with Image.open(request.FILES['files[]']) as im:
        dimensions = "%sx%s" % im.size

    return JsonResponse(
        {"src": "/media/tmp/%s_%s" % (uuid, filename),
         "filesize": format_bytes(filesize),
         "dimensions": dimensions,
         "filename": filename,
         "value": "tmp/%s_%s" % (uuid, filename)})
