"""Group Notifications."""
from happening.notifications import Notification


class GroupJoinedNotification(Notification):

    """Someone has joined a group you're in."""

    required_data = ["event", "group_name", "user", "user_name",
                     "user_photo_url"]
    category = "Groups"


class GroupLeftNotification(Notification):

    """Someone has left a group you're in."""

    required_data = ["event", "group_name", "user", "user_name",
                     "user_photo_url"]
    category = "Groups"


class GroupEditedNotification(Notification):

    """Someone has edited a group you're in."""

    required_data = ["event", "group_name", "user", "user_name",
                     "user_photo_url"]
    category = "Groups"
