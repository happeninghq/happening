"""General Happening views."""
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from happening.utils import format_bytes
from uuid import uuid4
from PIL import Image
from django.core.files.storage import default_storage


@require_POST
def file_upload(request):
    """Handle an ajax file upload."""
    uuid = uuid4().hex
    filename = request.FILES['files[]'].name
    filepath = 'tmp/%s_%s' % (uuid, filename)
    with default_storage.open(filepath, 'wb+') as destination:
        for chunk in request.FILES['files[]'].chunks():
            destination.write(chunk)

    filesize = default_storage.size(filepath)

    request.FILES['files[]'].seek(0)
    with Image.open(request.FILES['files[]']) as im:
        dimensions = "%sx%s" % im.size

    return JsonResponse(
        {"src": "/media/tmp/%s_%s" % (uuid, filename),
         "filesize": format_bytes(filesize),
         "dimensions": dimensions,
         "filename": filename,
         "value": "tmp/%s_%s" % (uuid, filename)})
