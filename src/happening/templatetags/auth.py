"""Template tags relating to authentication."""

from django import template
from allauth.socialaccount.models import SocialApp

register = template.Library()


@register.filter()
def provider_enabled(provider):
    """Check if the auth provider is enabled."""
    return SocialApp.objects.filter(provider=provider.id).first() is not None


@register.filter()
def providers_enabled(n):
    """Check if any auth provider is enabled."""
    return SocialApp.objects.count() > 0
