"""Period tasks related to emails."""

from periodically.decorators import hourly
from models import Email
from datetime import datetime


@hourly()
def send_emails():
    """Send emails which are active."""
    now = datetime.now()
    for email in Email.objects.all().filter(
            start_sending__lt=now,
            stop_sending__gt=now):
        email.send_all()
