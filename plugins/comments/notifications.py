"""Comment Notifications."""
from happening.notifications import Notification


class CommentNotification(Notification):

    """Someone has made a comment."""

    required_data = ["comment", "author_photo_url"]
    category = "Comments"
