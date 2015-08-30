"""Notification models."""
from django.db import models
from happening import db
from django.template.loader import render_to_string
import json
from cached_property import threaded_cached_property
from bs4 import BeautifulSoup
from django.utils import timezone
from markdown_deux import markdown
from happening.utils import convert_to_camelcase
from django.core.mail import send_mail
from django.conf import settings
from happening import notifications
from configuration import NotificationsEmailAddress
from django.contrib.sites.models import Site
from configuration import EmailFooter, EmailHeader
from django.template import Context, Template


class NotificationManager(models.Manager):

    """Custom Notification manager for unread."""

    def unread(self):
        """Get unread notifications."""
        return self.ordered().filter(read=False)

    def mark_all_as_read(self):
        """Mark all notifications as read."""
        for n in self.unread():
            n.read = True
            n.read_datetime = timezone.now()
            n.save()

    def ordered(self):
        """Return time-ordered notifications."""
        return self.all().order_by("-sent_datetime")


class Notification(db.Model):

    """A notification sent to a user."""

    objects = NotificationManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="notifications")
    template = models.CharField(max_length=200)
    data = models.TextField()
    sent_datetime = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        """Return the notification detail."""
        return "Notification (%s to %s)" % (self.template, self.user)

    @property
    def data2(self):
        """Deserialize data."""
        return json.loads(self.data)

    @data2.setter
    def data2(self, value):
        """Serialize data."""
        self.data = json.dumps(value)

    @threaded_cached_property
    def _rendered_notification(self):
        notification_name = convert_to_camelcase(self.template) +\
            "Notification"
        n = [c for c in notifications.Notification.__subclasses__() if
             c.__name__ == notification_name]

        if len(n) == 0:
            return None

        n = n[0]

        d = self.data2
        d["site"] = Site.objects.first().happening_site

        data = render_to_string("notifications/notifications/" +
                                n.category.lower() + "/" +
                                self.template + ".html", d)
        return data

    def url(self):
        """Return the URL this notification links to."""
        soup = BeautifulSoup(self.full)
        return soup.find(id="main-link")['href']

    @threaded_cached_property
    def image(self):
        """Return the image for this notification."""
        if not self._rendered_notification:
            return None
        return self._rendered_notification.split("<notification_image>")[1]\
                   .split("</notification_image>")[0]

    @threaded_cached_property
    def full(self):
        """Return the full text for this notification."""
        if not self._rendered_notification:
            return None
        return self._rendered_notification.split("<notification_text>")[1]\
                   .split("</notification_text>")[0]

    @threaded_cached_property
    def email_text(self):
        """Return the text email for this notification."""
        if not self._rendered_notification:
            return None
        content = self._rendered_notification.split("<notification_email>")[1]\
                      .split("</notification_email>")[0]
        if content:
            return content

        # If there is no content, for now just send the notification title
        return "You have a " + self.template + " notification."

    @threaded_cached_property
    def email_html(self):
        """Return the text email for this notification."""
        if not self._rendered_notification:
            return None
        content = self._rendered_notification.split("<notification_email>")[1]\
                      .split("</notification_email>")[0]
        if content:
            return markdown(content)
        else:
            return self.full

    @threaded_cached_property
    def subject(self):
        """Return the email subject for this notification."""
        if not self._rendered_notification:
            return None
        return self._rendered_notification.split("<notification_subject>")[1]\
                   .split("</notification_subject>")[0]

    @threaded_cached_property
    def short(self):
        """Return the short text for this notification."""
        soup = BeautifulSoup(self.full)
        for match in soup.findAll("a"):
            match.name = "strong"
            match.attrs = {}
            # match.replaceWithChildren()
        return str(soup)

    def email_notification(self):
        """Send an email of the notification to the user."""
        # First we need to render the header and footer
        # Then we can provide it to the template to do a text/html version

        header = Template(EmailHeader().get()).render(
            Context({"user": self.user}))
        footer = Template(EmailFooter().get()).render(
            Context({"user": self.user}))

        data = render_to_string("notifications/email.html",
                                {"notification": self,
                                 "email_header": header,
                                 "email_footer": footer})
        text_content = data.split("<email_text>")[1].split("</email_text>")[0]
        html_content = data.split("<email_html>")[1].split("</email_html>")[0]
        send_mail(self.subject,
                  text_content,
                  NotificationsEmailAddress().get(),
                  [self.user.email],
                  html_message=html_content)


class NotificationPreferenceManager(models.Manager):

    """Custom Notification manager for unread."""

    def get_with_default(self, notification):
        """Get notification."""
        notification = convert_to_camelcase(notification)
        notification_name = notification + "Notification"
        notification_type = [c for c in
                             notifications.Notification.__subclasses__() if
                             c.__name__ == notification_name][0]

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


class NotificationPreference(db.Model):

    """A user's notification preference."""

    objects = NotificationPreferenceManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="notification_preferences")
    notification = models.CharField(max_length=255)
    send_notifications = models.BooleanField(default=True)
    send_emails = models.BooleanField(default=True)
