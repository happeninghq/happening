"""Notifications."""
from happening.utils import convert_to_underscore, dump_django
from django.contrib.contenttypes.models import ContentType


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
        for k in data.keys():
            if k not in self.required_data and k not in self.optional_data:
                raise Exception("%s not expected" % k)

    def send(self):
        """Send the notification."""
        model_ct = ContentType.objects.get(app_label="notifications",
                                           model="notification")
        notification_model = model_ct.model_class()
        class_name = self.__class__.__name__
        template = convert_to_underscore(class_name)

        if template.endswith('_notification'):
            template = template[:-13]

        n = notification_model(user=self.recipient,
                               data=dump_django(self.data),
                               template=template)

        # If we should show it, we save the notification
        notification_preferences = self.recipient.notification_preferences.\
            get_with_default(template)

        if notification_preferences['send_notifications']:
            n.save()

        # If we should email it, we do so
        if notification_preferences['send_emails']:
            n.email_notification()


class EventInformationNotification(Notification):

    """An event you have tickets to is coming up."""

    required_data = ["event", "event_name", "time_to_event",
                     "is_final_notification", "is_voting"]
    category = "Events"


class CancelledTicketNotification(Notification):

    """You have cancelled your tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class EditedTicketNotification(Notification):

    """You have edited your tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class PurchasedTicketNotification(Notification):

    """You have purchased tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class MembershipPaymentSuccessfulNotification(Notification):

    """Your membership payment has been received."""

    required_data = ["amount"]
    category = "Membership"


class AdminEventMessageNotification(Notification):

    """A message from administrators regarding an event."""

    required_data = ["message", "event_name"]
    optional_data = ["subject"]
    category = "Events"

    send_notification = False
    can_edit_send_notification = False


class AdminMessageNotification(Notification):

    """A message from administrators."""

    required_data = ["message"]
    optional_data = ["subject"]

    send_notification = False
    can_edit_send_notification = False
