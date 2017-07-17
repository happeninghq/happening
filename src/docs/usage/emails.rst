.. _emails:

Emails
=======

**Sending Emails**

To send an email to all members, go to the ``Send Email`` page of the Staff panel. Emails have a query to specify who should recieve the email (see :ref:`filtering`), and a start and end time. Any members who match the query between the start and end time will recieve the email. Each member will only recieve each email a maximum of 1 time.

This is different to how most email systems work - where they are sent once when the email is written. In an event management system this is most useful for emails with event information, where latecomers would otherwise not get the email.

The ``to`` query is written using the Happening Query Language. More information is available at :ref:`filtering`.

**Sending Emails Related to an Event**

To send an email to all attendees of a given Event, visit the Event's page on the Staff panel (see :ref:`events`) and click ``Send Email``. This form is identical to the general ``Send Email`` form, but the ``content`` fields will have an ``event`` variable in context, which can be used e.g. ``Our event {{event.title}} will be....``.

**Automatic Emails**

Events can configure emails which will be sent automatically. These are configured when creating the Event and will have their start sending/stop sending set relative to the event. This are typically used for reminder and information emails.

In the ``to`` field, you may use ``{{event.id}}`` to represent the event ID and it will be automatically converted into the actual event ID.

(e.g. to send an email to all attendees of the event who have not cancelled their tickets, the query should be ``tickets__has:(event__id:{{event.id}} cancelled:False)``). For more information about filtering see :ref:`filtering`.