Blocks
========

Blocks provide spaces where plugins can add additional content to a page. Happening provides a number of blocks which can be exploited by plugins and several plugins offer blocks of their own which can be exploited by other plugins.


**Creating A Block**

To create a block, import the ``plugins`` library in a template and then use the ``plugin_block`` templatetag, providing the name of the block and any parameters to be passed to the block.

For example::

    {% load plugins %}
    {% plugin_block "events.event_long" event %}

This creates a block named "events.event_long" which passes an event as a parameter.

**Using A Block**

To use a block, create a file named ``blocks.py`` inside any app/plugin. Inside this file, import the ``plugin_block`` decorator from ``happening.plugins`` and use it as so::

    from happening.plugins import plugin_block
    from django.template.loader import render_to_string
    from django.template import RequestContext


    @plugin_block("events.event_long")
    def event_long(request, event):
        """Add groups to long event information."""
        return render_to_string("groups/blocks/events/event_long.html",
                                {"event": event},
                                context_instance=RequestContext(request))

This will add the rendered template to the ``events.event_long`` block. Using render_to_string to use templates is a useful technique with blocks but is not required.

**Built-in Blocks**

.. function:: events.event_long(request, event)

   Shown on the events page.

   :param request: Django request
   :param event: Event

.. function:: events.event_short(request, event)

   Shown on the index page next to a future event.

   :param request: Django request
   :param event: Event

.. function:: staff.event.buttons(request, event)

   Shown at the top of the staff event page, alongside "Send Email", "Manage Check Ins", etc.

   :param request: Django request
   :param event: Event

.. function:: staff.event.tickets.headers(request, event, ticket)

   Shown in the <thead><tr> of the ticket list on the staff event page

   :param request: Django request
   :param event: Event
   :param ticket: Ticket

.. function:: staff.event.tickets.info(request, event, ticket)

   Shown in the <tbody><tr> of the ticket list on the staff event page

   :param request: Django request
   :param event: Event
   :param ticket: Ticket

.. function:: staff.event.tickets.options(request, event, ticket)

   Shown in a button group to the right of each ticket on the staff event page. To fit the style this should return a <li> containing an <a> with a class of "button"

   :param request: Django request
   :param event: Event
   :param ticket: Ticket

.. function:: staff.event(request, event)
   
   Shown at the bottom of the staff event page

   :param request: Django request
   :param event: Event

.. function:: happening.footer(request)

   Shown at the footer of every page

   :param request: Django request
