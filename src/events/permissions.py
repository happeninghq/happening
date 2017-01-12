"""Event permissions."""

from happening.permissions import register_permission

register_permission(
    "Events",
    "create_event",
    "Create an event",
    "Can create a new event.")
