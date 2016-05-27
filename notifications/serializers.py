from models import Notification
from happening.serializers import Serializer


class NotificationSerializer(Serializer):
    """Notification serializer."""

    class Meta:
        model = Notification
        fields = ('url', 'user')
