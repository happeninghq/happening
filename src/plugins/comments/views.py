"""Comment views."""
from django.shortcuts import redirect, get_object_or_404, render
from events.models import Event
from .forms import CommentForm
from django.core.signing import Signer
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from happening.utils import get_model
from .notifications import CommentNotification
from happening.notifications import notify_following

signer = Signer()


def event_discussion(request, pk):
    """Discuss an event."""
    event = get_object_or_404(Event, pk=pk)

    follow_code = ""
    user_is_following = False
    if request.user.is_authenticated():
        follow_code = request.user.follow_object_code(event, "discuss")
        user_is_following = request.user.is_following(event, "discuss")

    return render(request, "comments/events/discussion.html",
                  {"event": event, "follow_code": follow_code,
                   "user_is_following": user_is_following})


@require_POST
@login_required
def post_comment(request):
    """Create a new comment."""
    parent_info = signer.unsign(request.POST['parent']).split(":")
    app_label = parent_info[0]
    model = parent_info[1]
    parent_object_id = parent_info[2]
    user_id = parent_info[3]

    if not request.user.pk == int(user_id):
        return HttpResponseForbidden()

    parent_content_type = ContentType.objects.get(
        app_label=app_label, model=model)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.parent_content_type = parent_content_type
        comment.parent_object_id = parent_object_id
        comment.save()

        # Add to messages
        messages.success(request, "Comment added.")

        # Subscribe the user to future comments
        parent_object_type = get_model(app_label, model)
        parent = parent_object_type.objects.get(pk=parent_object_id)
        request.user.follow(parent, "discuss")

        # Send notifications
        notify_following(
            parent, "discuss", CommentNotification,
            {"comment": comment,
             "author_photo_url": comment.author.profile.photo_url(),
             "author_name": str(comment.author),
             "object_name": str(parent),
             "object_url": request.POST['next']},
            ignore=[request.user])

        # Redirect
        return redirect(request.POST['next'])

    return redirect("index")
