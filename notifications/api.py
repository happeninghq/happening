from models import Notification
from serializers import NotificationSerializer
from rest_framework.decorators import list_route
from django.shortcuts import redirect
from happening.api import Api


class NotificationApi(Api):
    """Notification API."""

    model = Notification
    serializer_class = NotificationSerializer

    @list_route(methods=['post'])
    def mark_as_read(self, request):
        """Mark all of a user's notifications as read."""
        for n in self.get_queryset():
            n.mark_as_read()
        return redirect("notification-list")
