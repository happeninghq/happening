Creating Plugins
=================

To create a plugin, create a directory in the ``plugins`` directory and inside it create a ``__init__.py`` file. Inside this file create a class ``Plugin``::
    
    class Plugin(object):

        """Plugin which adds comments."""

        name = "Comments"

At a minimum, you must give a name attribute which will show in the "Plugins" page of the Admin panel. If you provide a docstring that will also be shown.

**URLS**

If you want to have views, add a ``url_root`` attribute to your ``Plugin`` class::

    url_root = "comments/"

In this case, it will prefix all URLs for this plugin with "comments/". Then create a urls.py as you would normally in a django project::

    from django.conf.urls import patterns, include

    urlpatterns = patterns('plugins.comments.views',
                           (r'^comments/posted/$', 'comment_posted'),
                           (r'^comments/', include('django_comments.urls')),
                           )

**Staff**

If you want to add views accessible only to staff, add a ``staff_url_root`` attribute to the ``Plugin`` class::
    
    staff_url_root = "groups/"

and then create a ``staff.py`` which contains the django urls::
    
    from django.conf.urls import patterns, url

    urlpatterns = patterns('plugins.groups.views',
                       url(r'^groups$',
                           'groups',
                           name='groups'),
                       )

These urls will only be accessible by staff members. If you want to add a link to the Staff panel navigation, inside ``staff.py`` add a ``staff_links`` variable::
    
    staff_links = (
        ("Groups", "groups"),
    )

The first part of the tuple is the text, the second part is the url name to link to.

**Admin**

If you want to add views accessible only to admins, add an ``admin_url_root`` attribute to the ``Plugin`` class::
    
    admin_url_root = "groups/"

and then create a ``admin.py`` which contains the django urls::
    
    from django.conf.urls import patterns, url

    urlpatterns = patterns('plugins.groups.views',
                       url(r'^group_admin$',
                           'group_admin',
                           name='group_admin'),
                       )

These urls will only be accessible by admins. If you want to add a link to the Admin panel navigation, inside ``admin.py`` add an ``admin_links`` variable::
    
    admin_links = (
        ("Groups", "group_admin"),
    )

The first part of the tuple is the text, the second part is the url name to link to.