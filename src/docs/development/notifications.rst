Notifications
===============

Notifications are used for communicating events to users. To create a new notification type create a file named ``notifications.py`` in any app, and add a new subclass of ``happening.notifications.Notification``. You must also create a template in ``templates/notifications/`` which will provide the layout for the notifications pages. *Check existing notifications for examples.*

When the data passed to notifications is serialized a shallow copy will be made. This means that in your notification templates, functions and properties will not be available, and references to other models will be flattened into an ID. If, for example, you require the user and user.profile, BOTH of these must be required by your notification.

To send a notification create an instance of your class (ensuring you provide the required parameters and no unexpected parameters) and then call ``.send()``::

    n = CancelledTicketNotification(
                    self.user,
                    ticket=self,
                    event=self.event,
                    event_name=str(self.event))
    n.send()