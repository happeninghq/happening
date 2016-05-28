Actions
==========

Actions allow plugins to respond to actions occuring within Happening. They are similar to `Django signals <https://docs.djangoproject.com/en/1.8/topics/signals/>`_.

**Triggering Actions**

To trigger an action (creating a point for plugins to respond), import ``happening.plugins.trigger_action`` and call it, passing the name of the action first, and keyword arguments which will be passed along to responders.

For example::

    from happening.plugins import trigger_action
    trigger_action("events.ticket_cancelled", ticket=self)

**Responding To Actions**

To respond to an action, create a file named ``actions.py`` in any app/plugin. In it, import the ``happening.plugins.action`` decorator and apply it like so::
    
    from happening.plugins import action

    @action("events.ticket_cancelled")
    def ticket_cancelled(ticket):
        """If a ticket is cancelled, ensure that it is not in any groups."""
        for g in ticket.groups.all():
            g.delete()

In this case, we will respond to the ticket cancelled action by deleting any groups attached to the ticket.

**Built-in Actions**

.. function:: events.ticket_cancelled(ticket)

   A ticket has been cancelled

   :param ticket: Ticket