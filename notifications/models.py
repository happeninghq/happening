""" Notification models. """
from django.db import models
from django.template.loader import render_to_string
import json
from cached_property import threaded_cached_property
from bs4 import BeautifulSoup
from datetime import datetime
from markdown_deux import markdown
from website.utils import convert_to_camelcase
import notifications
from django.core.mail import send_mail


class NotificationManager(models.Manager):

    """ Custom Notification manager for unread. """

    def unread(self):
        """ Get unread notifications. """
        return self.ordered().filter(read=False)

    def mark_all_as_read(self):
        """ Mark all notifications as read. """
        for n in self.unread():
            n.read = True
            n.read_datetime = datetime.now()
            n.save()

    def ordered(self):
        """ Return time-ordered notifications. """
        return self.all().order_by("-sent_datetime")


class Notification(models.Model):

    """ A notification sent to a user. """

    objects = NotificationManager()

    user = models.ForeignKey("auth.User", related_name="notifications")
    template = models.CharField(max_length=200)
    data = models.TextField()
    sent_datetime = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        """ Return the notification detail. """
        return "Notification (%s to %s)" % (self.template, self.user)

    @property
    def data2(self):
        """ Deserialize data. """
        return json.loads(self.data)

    @data2.setter
    def data2(self, value):
        """ Serialize data. """
        self.data = json.dumps(value)

    @threaded_cached_property
    def _rendered_notification(self):
        notification_name = convert_to_camelcase(self.template) +\
            "Notification"
        n = getattr(notifications, notification_name)

        data = render_to_string("notifications/notifications/" +
                                n.category.lower() + "/" +
                                self.template + ".html", self.data2)
        return data

    def url(self):
        """ Return the URL this notification links to. """
        soup = BeautifulSoup(self.full)
        return soup.find(id="main-link")['href']

    @threaded_cached_property
    def image(self):
        """ Return the image for this notification. """
        return self._rendered_notification.split("<notification_image>")[1]\
                   .split("</notification_image>")[0]

    @threaded_cached_property
    def full(self):
        """ Return the full text for this notification. """
        return self._rendered_notification.split("<notification_text>")[1]\
                   .split("</notification_text>")[0]

    @threaded_cached_property
    def email_text(self):
        """ Return the text email for this notification. """
        content = self._rendered_notification.split("<notification_email>")[1]\
                      .split("</notification_email>")[0]
        if content:
            return content

        # If there is no content, for now just send the notification title
        return "You have a " + self.template + " notification." +\
               " Visit https://www.southamptoncodedojo.com to check it."

    @threaded_cached_property
    def email_html(self):
        """ Return the text email for this notification. """
        content = self._rendered_notification.split("<notification_email>")[1]\
                      .split("</notification_email>")[0]
        if content:
            return markdown(content)
        else:
            return self.full

    @threaded_cached_property
    def subject(self):
        """ Return the email subject for this notification. """
        return self._rendered_notification.split("<notification_subject>")[1]\
                   .split("</notification_subject>")[0]

    @threaded_cached_property
    def short(self):
        """ Return the short text for this notification. """
        soup = BeautifulSoup(self.full)
        for match in soup.findAll("a"):
            match.name = "strong"
            match.attrs = {}
            # match.replaceWithChildren()
        return str(soup)

    def email_notification(self):
        """ Send an email of the notification to the user. """
        data = render_to_string("notifications/email.html",
                                {"notification": self})
        text_content = data.split("<email_text>")[1].split("</email_text>")[0]
        html_content = data.split("<email_html>")[1].split("</email_html>")[0]
        send_mail(self.subject,
                  text_content,
                  "admin@southamptoncodedojo.com",
                  [self.user.email],
                  html_message=html_content)


class NotificationPreferenceManager(models.Manager):

    """ Custom Notification manager for unread. """

    def get_with_default(self, notification):
        """ Get notification. """
        notification = convert_to_camelcase(notification)
        notification_name = notification + "Notification"
        notification_type = getattr(notifications, notification_name)

        to_return = {
            "send_notifications": notification_type.send_notification,
            "send_emails": notification_type.send_email}

        n = self.all().filter(notification=notification).first()
        if n:
            if notification_type.can_edit_send_notification:
                to_return["send_notifications"] = n.send_notifications
            if notification_type.can_edit_send_email:
                to_return["send_emails"] = n.send_emails

        return to_return


class NotificationPreference(models.Model):

    """ A user's notification preference. """

    objects = NotificationPreferenceManager()

    user = models.ForeignKey("auth.User",
                             related_name="notification_preferences")
    notification = models.CharField(max_length=255)
    send_notifications = models.BooleanField(default=True)
    send_emails = models.BooleanField(default=True)
