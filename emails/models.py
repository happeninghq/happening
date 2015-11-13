"""Email models."""
from django.db import models
from happening import db
from django.conf import settings
from django.utils import timezone
from happening import filtering
from events.models import Event
from emails.notifications import EmailNotification
from emails import render_email


class Email(db.Model):
    """An instruction to send a templated email."""

    # Optionally link the email to an event
    event = models.ForeignKey(Event, null=True)
    # This is a query
    to = models.TextField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    start_sending = models.DateTimeField()
    stop_sending = models.DateTimeField()
    disabled = models.BooleanField(default=False)

    class Meta:
        # Needed because this is loaded early
        app_label = 'emails'

    @property
    def status(self):
        """Return Completed/Active/Pending depending on start and end dates."""
        if self.disabled:
            return "Disabled"
        now = timezone.now()
        if self.stop_sending < now:
            return "Completed"
        elif self.start_sending < now:
            return "Active"
        return "Pending"

    def send(self, user):
        """Send the email to a user, if they haven't already received it."""
        if self.sent_emails.filter(user=user).count() > 0:
            return

        EmailNotification(user,
                          subject=render_email(self.subject, user, self.event),
                          content=render_email(self.content, user, self.event)
                          ).send()

        SentEmail(email=self, user=user).save()

    def send_all(self):
        """Send the email to all eligible users."""
        for user in filtering.query(self.to):
            self.send(user)

    def save(self):
        """Automatically send emails if required."""
        # Do any replacements needed in the "to"

        if self.event:
            self.to = self.to.replace("{{event.id}}", str(self.event.pk))\
                             .replace("{{event.pk}}", str(self.event.pk))

        is_new = True if self.pk is None else False
        super(Email, self).save()
        if is_new and self.start_sending < timezone.now() < self.stop_sending:
            self.send_all()


class SentEmail(db.Model):
    """An Email sent to a User."""

    email = models.ForeignKey(Email, related_name="sent_emails")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="received_emails")
    sent_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Needed because this is loaded early
        app_label = 'emails'
