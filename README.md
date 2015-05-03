Happening
=========

[![Build Status](https://travis-ci.org/jscott1989/happening.svg?branch=master)](https://travis-ci.org/jscott1989/happening)
[![Coverage Status](https://coveralls.io/repos/jscott1989/happening/badge.svg?branch=master)](https://coveralls.io/r/jscott1989/happening?branch=master)

This is a WIP project for Happening: an open source event/community management tool.

Think Eventbrite meets Meetup, running on your own domain with your own branding.

Pull requests are welcomed.

Requirements
-------
The following must be available and configured:
* python
* virtualenv

Development Requirements
--------
* jshint (Available via: npm install -g jshint)

Getting started
--------
Clone the repository to your disk, and then run setup - this will download 
all requirements and set up the database with some sample events (from [Southampton Code Dojo](https://southamptoncodedojo.com)).

Coding Conventions
-------
For Python, follow [PEP8](http://www.python.org/dev/peps/pep-0008/) and
[PEP257](http://www.python.org/dev/peps/pep-0257/). Check that the code
passes using check-standards

check-standards also looks for common mistakes such as unused or double
imports - so try to fix these issues as they are noticed. If any method has a
higher cyclomatic complexity than 10 check-standards will flag it and it
should be changed (split up into multiple methods).

Requirements files should be separated into logical groups, with each
individual requirement commented. All requirements should specify a version.

All functionality implemented should have tests, and all code should follow the
coding conventions mentioned above.

Code coverage should not fall below 90%.

Flash messages
-------
Flash messages are used to indicate the success/failure of an action (for example, posting a comment, purchasing a ticket, etc.). To manage flash messages we use the django messages framework.

```
from django.contrib import messages
messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')
```

Notifications
-------
Notifications are used for communicating events to users. To create a new notification
type create a file named notifications.py in any app, and add a new subclass of
happening.notifications.Notification. You must also create a template in
templates/notifications/ which will provide the layout for the notifications pages.
Check existing notifications for examples.

When the data passed to notifications is serialized a shallow copy will be made. This means that in your notification templates, functions and properties will not be available, and references to other models will be flattened into an ID. If, for example, you require the user and user.profile, BOTH of these must be required by your notification.

To send a notification create an instance of your class (ensuring you provide 
the required parameters and no unexpected parameters) and then call .send()

e.g.

```
n = CancelledTicketNotification(
                self.user,
                ticket=self,
                event=self.event,
                event_name=str(self.event))
n.send()
```


Configuration
-------
Configuration is used to allow site-by-site configuration variables. To create a configuration
variable create a file named configuration.py in any app. In this file, add a subclass of
happening.configuration.ConfigurationVariable representing the variable you are adding.

For example:

```
class NameOfEvents(configuration.CharField):

    """The term used to refer to an event, e.g. "match", "rally"."""

    default = "event"
```

This creates a "name of events" variable which is a string (CharField), and defaults to "event"

To access the content of the variable, create an instance of the class and call .get()

e.g.
``` event_name = NameOfEvents().get() ```

In a template, use the get_configuration filter in the plugins library to read configuration
variables.

e.g.
```
    {% load plugins %}
    {{"pages.configuration.NameOfEvents"|get_configuration}}
```


Event Configuration
-------
Event Configuration is used to allow event-by-event configuration variables. To create a configuration
variable create a file named event_configuration.py in any app. In this file, add a subclass of
happening.configuration.ConfigurationVariable representing the variable you are adding.

For example:

```
class GroupCreation(configuration.ChoiceField):

    """Who is able to create groups."""

    default = 0

    choices = [
        (0, "Members cannot create groups"),
        (1, "Members can create groups after the event starts"),
        (2, "Members can create groups at any time"),
    ]
```

This creates a "group creation" variable which is one of three options, and defaults to 0

To access the content of the variable, create an instance of the class and call .get()

e.g.
``` can_create_groups = GroupCreation(event).get() ```

In a template, use the get_configuration filter in the plugins library to read configuration
variables.

e.g.
```
    {% load plugins %}
    {{"groups.configuration.GroupCreation"|get_configuration:event}}
```