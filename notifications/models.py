""" Notification models. """
from django.db import models
from django.template.loader import render_to_string
import json
from cached_property import threaded_cached_property
from bs4 import BeautifulSoup
from datetime import datetime


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
        data = render_to_string("notifications/notifications/" +
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
    def short(self):
        """ Return the short text for this notification. """
        soup = BeautifulSoup(self.full)
        for match in soup.findAll("a"):
            match.name = "strong"
            match.attrs = {}
            # match.replaceWithChildren()
        return str(soup)


class NotificationPreference(models.Model):

    """ A user's notification preference. """

    user = models.ForeignKey("auth.User",
                             related_name="notification_preferences")
    notification = models.CharField(max_length=255)
    send_notifications = models.BooleanField(default=True)
    send_emails = models.BooleanField(default=True)
