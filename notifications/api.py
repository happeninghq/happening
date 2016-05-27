from models import Notification
from rest_framework import viewsets
from serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """Notification API."""

    queryset = Notification.objects.all().order_by('-sent_datetime')
    serializer_class = NotificationSerializer
