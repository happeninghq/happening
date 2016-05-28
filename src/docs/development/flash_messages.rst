.. _dev_flash_messages:

Flash Messages
================

Flash messages are used to indicate the success/failure of an action (for example, posting a comment, purchasing a ticket, etc.). To manage flash messages we use the `django messages framework <https://docs.djangoproject.com/en/1.8/ref/contrib/messages/>`_::

    from django.contrib import messages
    messages.debug(request, '%s SQL statements were executed.' % count)
    messages.info(request, 'Three credits remain in your account.')
    messages.success(request, 'Profile details updated.')
    messages.warning(request, 'Your account expires in three days.')
    messages.error(request, 'Document deleted.')