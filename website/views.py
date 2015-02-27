""" General website views. """

from django.shortcuts import redirect, get_object_or_404
from django_comments.models import Comment


def comment_posted(request):
    """ A comment has been posted. Redirect back to it. """
    comment = get_object_or_404(Comment, pk=request.REQUEST['c'])
    return redirect(comment.content_object.get_absolute_url() +
                    "#c" + request.REQUEST['c'])
