"""Comment views."""
from django.shortcuts import redirect, get_object_or_404, render
from events.models import Event
from forms import CommentForm
from django.core.signing import Signer
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden

signer = Signer()


def event_discussion(request, pk):
    """Discuss an event."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "comments/events/discussion.html",
                  {"event": event})


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

        # Redirect
        return redirect(request.POST['redirect_url'])

    return redirect("index")
