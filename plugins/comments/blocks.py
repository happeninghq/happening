"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from django.template import RequestContext
from event_configuration import CommentOnGroups


@plugin_block("events.event.secondary_navigation")
def event_secondary_navigation(request, secondary_nav, event):
    """Add discussion to event page."""
    return render_to_string(
        "comments/blocks/events/event/secondary_navigation.html",
        {"secondary_nav": secondary_nav, "event": event},
        context_instance=RequestContext(request))


@plugin_block("events.event_block.small_info")
def event_block_small_info(request, event):
    """Add comment count to event block."""
    return render_to_string(
        "comments/blocks/events/event_block/small_info.html",
        {"event": event}, context_instance=RequestContext(request))


@plugin_block("events.event.primary_content")
def event_primary_content(request, event):
    """Add discussion to event info."""
    recent_comments = [a for a in event.comments()][:3]
    return render_to_string(
        "comments/blocks/events/event/primary_content.html",
        {"event": event, "recent_comments": recent_comments},
        context_instance=RequestContext(request))


@plugin_block("groups.group.primary_content")
def groups_group_primary_content(request, group):
    """Show additional information on groups."""
    if not CommentOnGroups(object=group.event).get():
        return ""

    follow_code = ""
    user_is_following = False
    if request.user.is_authenticated():
        follow_code = request.user.follow_object_code(group, "discuss")
        user_is_following = request.user.is_following(group, "discuss")

    return render_to_string(
        "comments/blocks/groups/group/primary_content.html",
        {"group": group, "follow_code": follow_code,
         "user_is_following": user_is_following,
         "request": request})
