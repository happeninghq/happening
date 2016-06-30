"""Notification models."""
from django.db import models
from happening import db
from django.template.loader import render_to_string
import json
from cached_property import threaded_cached_property
from bs4 import BeautifulSoup
from django.utils import timezone
from markdown_deux import markdown
from happening.utils import convert_to_camelcase, externalise_urls
from django.core.mail import send_mail
from django.conf import settings
from happening import notifications
from .configuration import NotificationsEmailAddress
from django.contrib.sites.models import Site
from .configuration import EmailFooter, EmailHeader
from django.template import Context, Template


class NotificationManager(db.Manager):

    """Custom Notification manager for unread."""

    def unread(self):
        """Get unread notifications."""
        return self.ordered().filter(read=False)

    def ordered(self):
        """Return time-ordered notifications."""
        return self.all().order_by("-sent_datetime")

    def get_for_user(self, user):
        """Return filtered for the user."""
        return self.filter(user=user)


class EmailableNotification(object):

    """A notification that can be emailed."""

    def __str__(self):
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
        d["happening_site"] = Site.objects.first().happening_site

        data = render_to_string("notifications/notifications/" +
                                n.category.lower() + "/" +
                                self.template + ".html", d)
        return data

    @threaded_cached_property
    def subject(self):
        """Return the email subject for this notification."""
        if not self._rendered_notification:
            return None
        return self._rendered_notification.split("<notification_subject>")[1]\
                   .split("</notification_subject>")[0]

    def link_url(self):
        """Return the URL this notification links to."""
        soup = BeautifulSoup(self.full, "html.parser")
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
            return externalise_urls(content)

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
            return markdown(externalise_urls(content))
        else:
            return self.full

    @threaded_cached_property
    def short(self):
        """Return the short text for this notification."""
        soup = BeautifulSoup(self.full, "html.parser")
        for match in soup.findAll("a"):
            match.name = "strong"
            match.attrs = {}
            # match.replaceWithChildren()
        return str(soup)


class Notification(db.Model, EmailableNotification):

    """A notification sent to a user."""

    objects = NotificationManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="notifications")
    template = models.CharField(max_length=200)
    data = models.TextField()
    sent_datetime = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_datetime = models.DateTimeField(null=True)

    @staticmethod
    def has_write_permission(request):
        """Nobody can write notifications."""
        return False

    @staticmethod
    def has_read_permission(request):
        """Everyone can read notifications."""
        return True

    @staticmethod
    def has_mark_as_read_permission(request):
        """Every can mark their notifications as read."""
        return True

    def has_object_read_permission(self, request):
        """Can read their own notifications."""
        return request.user == self.user

    def mark_as_read(self):
        """Mark as read."""
        if not self.read:
            self.read = True
            self.read_datetime = timezone.now()
            self.save()


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
