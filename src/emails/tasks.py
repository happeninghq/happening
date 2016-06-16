"""Period tasks related to emails."""
from datetime import datetime
from happening.tasks import periodic_task
from datetime import timedelta


@periodic_task(run_every=timedelta(minutes=1))
def send_emails():
    """Send emails which are active."""
    from .models import Email
    now = datetime.now()
    for email in Email.objects.all().filter(
            start_sending__lt=now,
            stop_sending__gt=now,
            disabled=False):
        email.send_all()
