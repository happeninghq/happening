"""Comment template tags."""

from django import template
from django.template.loader import render_to_string
from django.template import RequestContext
from plugins.comments.forms import CommentForm
from django.core.signing import Signer
from django.contrib.contenttypes.models import ContentType
from plugins.comments.models import get_comments_for_object

signer = Signer()
register = template.Library()


@register.simple_tag(takes_context=True)
def comments(context, object):
    """Include comments."""
    comments = get_comments_for_object(object)
    return render_to_string(
        "comments/_comments.html",
        {"object": object, "comments": comments},
        context_instance=RequestContext(context['request']))


@register.simple_tag(takes_context=True)
def comments_form(context, object):
    """Include comments."""
    form = CommentForm()

    object_type = ContentType.objects.get_for_model(object)
    object_id = object.pk

    parent = signer.sign("%s:%s:%s:%s" % (object_type.app_label,
                                          object_type.model,
                                          object_id,
                                          context['request'].user.pk))

    return render_to_string(
        "comments/_form.html",
        {"form": form,
         "parent": parent},
        context_instance=RequestContext(context['request']))
