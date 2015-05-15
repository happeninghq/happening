.. _dev_configuration_variables:

Configuration Variables
=========================

Configuration Variables are used to allow plugins to add properties to existing models. In the core of Happening they are used to add general :ref:`dev_configuration`, and :ref:`dev_event_configuration`. :ref:`dev_plugins` can add their own configuration variables.

**Adding Configuration Variables**

To add a configuration variable, you must create a file in your app/plugin which is specified by the model you're attempting to add a property to. In the case of :ref:`dev_configuration` the filename is ``configuration.py``, in the case of :ref:`dev_event_configuration` it is ``event_configuration.py``, for :ref:`dev_plugins` see the appropriate documentation.

Inside this file, create classes which subclass ``happening.configuration.ConfigurationVariable``. There are a number of existing subclasses to provide useful data types, which are listed below.

**Accessing Configuration Variables**

In Python code, to access a configuration variable, simply instantiate the variable's class, passing the object the variable should be bound to, and then call .get()::
    
    from plugins.groups.event_configuration import GroupCreation
    event = # ...
    group_creation_config = GroupCreation(event).get()

In a template, use the get_configuration filter in the plugins library to read configuration variables::

    {% load plugins %}
    {{"pages.configuration.NameOfEvents"|get_configuration}}
    {{"groups.configuration.GroupCreation"|get_configuration:event}}

**Allowing Other Plugins to Add Configuration Variables**

If you wish to use configuration variables on your models, you will use the ``get_configuration_variables``, ``attach_to_form``, and ``save_variables`` methods.

An example usage is shown below::

    def edit_group(request, pk, group_number):
        """Edit a group."""
        event = # ...
        group = # ...
        variables = get_configuration_variables("group_form", group, event=event)
        form = GroupForm(instance=group)
        attach_to_form(form, variables)
        if request.method == "POST":
            form = GroupForm(request.POST, instance=group)
            attach_to_form(form, variables)
            if form.is_valid():
                form.save()
                save_variables(form, variables)
                return redirect("view_event", event.pk)
        return render(request, "groups/edit_group.html", {"form": form})

In this case, we are editing a group - and allowing Configuration Variables to be added to the group. We first get the variables using ``get_configuration_variables``, passing the filename which will contain the variables ("group_form.py"), the object that the variables will attach to (group) and some extra context which can optionally be used by the Configuration Variables (the event the group is for). After creating the form (or re-creating the form to add POST data) we must use ``attach_to_form`` to add the appropriate fields to the form. Once the form is validated we use ``save_variables`` to commit the variables to the database.

The process is very similar when we're creating a new object instead of modifying an existing one::
    
    def add_group(request, pk):
        """Add a group."""
        event = # ..
        form = GroupForm()
        variables = get_configuration_variables("group_form", event=event)
        attach_to_form(form, variables)

        if request.method == "POST":
            form = GroupForm(request.POST)
            attach_to_form(form, variables)
            if form.is_valid():
                group = form.save()
                variables = get_configuration_variables("group_form", group, event=event)
                save_variables(form, variables)
                return redirect("view_event", event.pk)
        return render(request, "groups/add_group.html", {"form": form, "event": event})

In here, we initially get the variables without specifying which group they will be attached to, then after we have validated the form and created the group, we get new variables which are bound to the group object, before saving them using ``save_variables``.

.. automodule:: happening.configuration
   :members: get_configuration_variables, attach_to_form, save_variables
   :noindex:


**Configuration Variable Types**

.. automodule:: happening.configuration
   :members: ConfigurationVariable, BooleanField, CharField, ChoiceField, EmailField, IntegerField, URLField
   :noindex:


**Custom Properties**

Custom Properties are a set of two Configuration Variable types ``CustomProperties`` and ``PropertiesField`` which work together to allow users to configure their own properties attached to models.

To demonstrate how these work, we'll take the example of adding custom properties to groups on an event-by-event basis. First, we add a ``CustomProperties`` to ``event_configuration.py``::
    
    from happening import configuration
    class GroupProperties(configuration.PropertiesField):

        """What properties should be provided for groups."""

Then, we add these properties (via a ``PropertiesField``) to the groups. To do this, we create a ``group_form.py``::
    
    from happening import configuration

    class CustomProperties(configuration.CustomProperties):

        """The custom properties added on event creation."""

        configuration_variable = "plugins.groups.event_configuration.GroupProperties"
        configuration_variable_instance = "event"

Here, the properties come from the configuration variable "plugins.groups.event_configuration.GroupProperties", and are bound to the "event" object (which will be passed in when calling ``get_configuration_variables``).

This is all that is needed to allow users to add their own properties to models.

.. automodule:: happening.configuration
   :members: CustomProperties, PropertiesField
   :noindex:

**Custom Variable Types**

Creating a custom variable type typically requires the creation of three classes. To demonstrate we'll create an "EpicEditorField", which is simply a TextArea with a particular class added (that Javascript can hook onto).

First, we must create a subclass of ``django.forms.Widget``, and implement the ``render`` method::

    class EpicEditorWidget(forms.Textarea):

        """A widget that uses EpicEditor."""

        def render(self, name, value, attrs):
            """Render the widget."""
            attrs['class'] = 'edit_markdown ' + attrs.get('class', '')
            return super(EpicEditorWidget, self).render(name, value, attrs)

In this case we have overridded forms.Textarea which is a subclass of forms.Widget and takes care of rendering a TextArea. We could have used render_to_string here to render completely custom html.

We then create a subclass of ``django.forms.Field``, which references the widget to be rendered. It's often best here to subclass an existing ``Field`` subclass (see ``Django Form Fields Documentation <https://docs.djangoproject.com/en/1.8/ref/forms/fields/>``_, of which there are many::

    class EpicEditorField(forms.CharField):

        """A field that uses an EpicEditor markdown editor."""

        widget = EpicEditorWidget

In this case we subclass CharField as the widget will return a text value.

Finally, you need to create a subclass of ``happening.configuration.ConfigurationVariable``. At a minimum this should point to the Field just created::
    
    class EpicEditorField(ConfigurationVariable):

        field = EpicEditorField

This could also be achieved without the ``ConfigurationVariable`` subclass. However, in this case you would be required to reference the ``Field`` subclass each time you create a new configuration variable of this type. For example::

    class Description(configuration.CharField):

        """Event Description."""

        field = forms.EpicEditorField

In this case, we simply override the field for the Description variable.

**Custom Variable Renderers**

With the previous example of the EpicEditorField, we allow the users to create markdown input using EpicEditor. However the output will need to be formatted as markdown each time it is used. To avoid this, we can create a subclass of the ``happening.configuration.Renderer`` class::
    
    class MarkdownRenderer(Renderer):

        """Render the markdown in a string."""

        def render(self, value):
            """Render the markdown in a string."""
            return mark_safe(markdown(value))

and then reference this in our variable/variable type::

    class EpicEditorField(ConfigurationVariable):

        field = forms.EpicEditorField
        renderer = MarkdownRenderer()

This will ensure that when using the default functionality for getting variables, it will get the rendered HTML rather than the raw markdown. This can also be used to format data in the correct type (boolean, int, etc.).

**Custom "Custom Properties" Types**

Currently Custom Properties can only have variables of type CharField, EmailField, IntegerField, URLField, and BooleanField. We hope to allow for custom types in future.
