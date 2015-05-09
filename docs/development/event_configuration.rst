Event Configuration
=====================

Event Configuration is used to allow event-by-event configuration variables. To create a configuration variable create a file named ``event_configuration.py`` in any app. In this file, add a subclass of ``happening.configuration.ConfigurationVariable`` representing the variable you are adding.

For example::

    class GroupCreation(configuration.ChoiceField):

        """Who is able to create groups."""

        default = 0

        choices = [
            (0, "Members cannot create groups"),
            (1, "Members can create groups after the event starts"),
            (2, "Members can create groups at any time"),
        ]

This creates a "group creation" variable which is one of three options, and defaults to 0

To access the content of the variable, create an instance of the class and call ``.get()``::
    
    can_create_groups = GroupCreation(event).get()

In a template, use the get_configuration filter in the plugins library to read configuration variables::

    {% load plugins %}
    {{"groups.configuration.GroupCreation"|get_configuration:event}}