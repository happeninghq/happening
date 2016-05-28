"""General Happening views."""
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from happening.utils import format_bytes
from uuid import uuid4
from PIL import Image
from happening.storage import storage
from django.conf import settings
from django.shortcuts import redirect
from django.core.signing import Signer
from django.http import HttpResponseForbidden
from happening.utils import get_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

signer = Signer()


@login_required
@require_POST
def file_upload(request):
    """Handle an ajax file upload."""
    uuid = uuid4().hex
    filename = request.FILES['files[]'].name
    filepath = 'tmp/%s_%s' % (uuid, filename)
    with storage.open(filepath, 'wb+') as destination:
        for chunk in request.FILES['files[]'].chunks():
            destination.write(chunk)

    filesize = storage.size(filepath)

    request.FILES['files[]'].seek(0)
    with Image.open(request.FILES['files[]']) as im:
        dimensions = "%sx%s" % im.size

    return JsonResponse(
        {"src": os.path.join(settings.MEDIA_URL, "tmp", uuid + "_" + filename),
         "filesize": format_bytes(filesize),
         "dimensions": dimensions,
         "filename": filename,
         "value": "tmp/%s_%s" % (uuid, filename)})


@login_required
@require_POST
def follow(request):
    """Follow an object."""
    object_info = signer.unsign(request.POST['object']).split(":")
    app_label = object_info[0]
    model = object_info[1]
    object_id = object_info[2]
    role = object_info[3]
    user_id = object_info[4]

    if not request.user.pk == int(user_id):
        return HttpResponseForbidden()

    obj_type = get_model(app_label, model)

    obj = obj_type.objects.get(pk=object_id)
    request.user.follow(obj, role, True)
    messages.success(request, request.POST['message'])
    return redirect(request.GET["next"])


@login_required
@require_POST
def unfollow(request):
    """Unfollow an object."""
    object_info = signer.unsign(request.POST['object']).split(":")
    app_label = object_info[0]
    model = object_info[1]
    object_id = object_info[2]
    role = object_info[3]
    user_id = object_info[4]

    if not request.user.pk == int(user_id):
        return HttpResponseForbidden()

    obj_type = get_model(app_label, model)

    obj = obj_type.objects.get(pk=object_id)

    request.user.unfollow(obj, role)
    messages.success(request, request.POST['message'])
    return redirect(request.GET["next"])
