""" Notification models. """
from django.db import models
from django.template.loader import render_to_string
import json
from cached_property import threaded_cached_property
from bs4 import BeautifulSoup


class Notification(models.Model):

    """ A notification sent to a user. """

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
