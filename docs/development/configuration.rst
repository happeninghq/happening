.. _dev_configuration:

Configuration
==============

Configuration is used to allow site-by-site :ref:`dev_configuration_variables`. To create a configuration variable create a file named ``configuration.py`` in any app. In this file, add a subclass of ``happening.configuration.ConfigurationVariable`` representing the variable you are adding.

For example::

    class NameOfEvents(configuration.CharField):

        """The term used to refer to an event, e.g. "match", "rally"."""

        default = "event"

This creates a "name of events" variable which is a string (CharField), and defaults to "event"

To access the content of the variable, create an instance of the class and call .get()::

    event_name = NameOfEvents().get()

In a template, use the get_configuration filter in the plugins library to read configuration variables::

    {% load plugins %}
    {{"pages.configuration.NameOfEvents"|get_configuration}}