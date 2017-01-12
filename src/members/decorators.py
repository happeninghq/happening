"""Member decorators."""
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


def require_editing_own_profile(f):
    """Require that the pk passed is equal to the current user's pk."""
    def inner_require_editing_own_profile(request, pk):
        member = get_object_or_404(get_user_model(), pk=pk)
        # TODO: replace with group permissions
        if not member == request.user and not request.user.is_staff:
            raise Http404
        return f(request, pk)
    return login_required(inner_require_editing_own_profile)
