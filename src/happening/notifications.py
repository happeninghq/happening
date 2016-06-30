"""Notifications."""
from happening.utils import convert_to_underscore, dump_django
from django.contrib.contenttypes.models import ContentType
from happening.models import Follow
from happening.filtering import EmailUser
from notifications.models import EmailableNotification


class Notification(object):

    """A notification that can be sent to a user."""

    required_data = []
    optional_data = []
    category = "General"

    can_edit_send_notification = True
    can_edit_send_email = True

    send_notification = True
    send_email = True

    def __init__(self, recipient, **data):
        """Specify the user to notify and the data to pass."""
        self.recipient = recipient
        self.data = data

        # Check that all required data is provided
        for k in self.required_data:
            if k not in data:
                raise Exception("%s is required" % k)

        # Check that no unexpected data is provided
        for k in list(data.keys()):
            if k not in self.required_data and k not in self.optional_data:
                raise Exception("%s not expected" % k)

    def send(self):
        """Send the notification."""
        class_name = self.__class__.__name__
        template = convert_to_underscore(class_name)

        if template.endswith('_notification'):
            template = template[:-13]

        if not isinstance(self.recipient, EmailUser):
            # This is a normal notification to a user
            model_ct = ContentType.objects.get(app_label="notifications",
                                               model="notification")
            notification_model = model_ct.model_class()
            n = notification_model(user=self.recipient,
                                   data=dump_django(self.data),
                                   template=template)
        else:
            n = EmailableNotification()
            n.user = self.recipient
            n.data = dump_django(self.data)
            n.template = template

        if not isinstance(self.recipient, EmailUser):
            # If we should show it, we save the notification
            notification_preferences = self.recipient.\
                notification_preferences.get_with_default(template)

            if notification_preferences['send_notifications']:
                n.save()

        # If we should email it, we do so
        if isinstance(self.recipient, EmailUser) or \
                notification_preferences['send_emails']:
            n.email_notification()


def notify_following(obj, role, notification, data, ignore=[]):
    """Notify those following the given object/role."""
    object_type = ContentType.objects.get_for_model(obj)
    follows = Follow.objects.filter(
        target_content_type=object_type,
        target_object_id=obj.pk,
        role=role,
        is_subscribed=True)

    for follow in follows:
        if follow.user not in ignore:
            n = notification(follow.user, **data)
            n.send()
