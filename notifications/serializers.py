from models import Notification
from happening.serializers import Serializer


class NotificationSerializer(Serializer):
    """Notification serializer."""

    class Meta:
        model = Notification
        fields = ('url', 'user', 'link_url', 'sent_datetime', 'read',
                  'read_datetime')
