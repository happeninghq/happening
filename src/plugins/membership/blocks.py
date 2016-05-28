"""Membership template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from django.template import RequestContext


@plugin_block("members.settings")
def members_settings(request, member):
    """Add current membership level and option to change."""
    return render_to_string("membership/blocks/members/settings.html",
                            {"member": member},
                            context_instance=RequestContext(request))


@plugin_block("members.member_image")
def members_member_image(request, member):
    """Add icon to member images if they have paid."""
    return render_to_string("membership/blocks/members/member_image.html",
                            {"member": member},
                            context_instance=RequestContext(request))


@plugin_block("members.profile.image")
def members_profile_image(request, member):
    """Add not to profile if they have paid."""
    return render_to_string("membership/blocks/members/profile/image.html",
                            {"member": member},
                            context_instance=RequestContext(request))
