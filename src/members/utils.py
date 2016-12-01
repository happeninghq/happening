"""Member utils."""
from members.configuration import AllowRegistration


def allow_new_users(request):
    """Are new users allowed to register."""
    return AllowRegistration().get()
