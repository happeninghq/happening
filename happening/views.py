"""General Happening views."""
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse
from happening.utils import format_bytes
from uuid import uuid4
from PIL import Image
import os


@require_POST
def file_upload(request):
    """Handle an ajax file upload."""
    uuid = uuid4().hex
    filename = request.FILES['files[]'].name
    filepath = '%s/tmp/%s_%s' % (settings.MEDIA_ROOT, uuid, filename)
    with open(filepath, 'wb+') as destination:
        for chunk in request.FILES['files[]'].chunks():
            destination.write(chunk)

    filesize = os.path.getsize(filepath)
    with Image.open(filepath) as im:
        dimensions = "%sx%s" % im.size

    return JsonResponse(
        {"src": "/media/tmp/%s_%s" % (uuid, filename),
         "filesize": format_bytes(filesize),
         "dimensions": dimensions,
         "filename": filename,
         "value": filepath})
