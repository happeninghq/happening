"""Member notifications."""
from happening.notifications import Notification


class MembershipPaymentSuccessfulNotification(Notification):

    """Your membership payment has been received."""

    required_data = ["amount"]
    category = "Membership"
