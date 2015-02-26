""" Notifications. """
from models import Notification as notification_model
from website.utils import convert_to_underscore, dump_django


class Notification(object):

    """ A notification that can be sent to a user. """

    required_data = []
    optional_data = []
    category = "Other"

    send_notification = True
    send_email = True

    def __init__(self, recipient, **data):
        """ Specify the user to notify and the data to pass. """
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
        """ Send the notification. """
        class_name = self.__class__.__name__
        template = convert_to_underscore(class_name)

        if template.endswith('_notification'):
            template = template[:-13]

        n = notification_model(user=self.recipient,
                               data=dump_django(self.data),
                               template=template)
        n.save()

# All notification types go under here


class CommentNotification(Notification):

    """ Someone has made a comment. """

    required_data = ["comment", "author_photo_url"]
    category = "Comments"
