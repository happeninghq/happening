.. _dev_following:

Following
==============

"Following" is used to allow users to optionally recieve updates about a particular thing. Currently this is only used for :ref:`dev_plugins_comments`, but it is abstract and can be used with anything.

A "role" allows for different users to follow different aspects of the same object. For example, many users may want to follow a discussion on an event, but relatively few users want to be alerted when new groups are created.

**Automatically Following**

To make a user follow a given object/role, use the ``follow`` method on the User instance::
    
    user.follow(event, "discuss")

**Manual Following**

Automatic following will not force the user to follow an object/role pair if they have previously chosen to unfollow. If you wish to force this follow (e.g. if the user has explicitly said they wish to follow it) then pass force=True::
    
    user.follow(event, "discuss", force=True)

alternatively, a view has been set up which can be pushed to and will deal with these manual follows. To use this first call ``follow_object_code`` on the User instance to generate a signed code (this ensures that users can only set up follows which are authorised)::

    code = user.follow_object_code(event, "discuss")

Then allow the user to POST this code to the "follow" view (as the "object" parameter). You should also pass a "next" GET parameter which tells the view where to redirect to, and the "message" parameter which will be sent as success :ref:`dev_flash_messages`..::
    
        <form action="{% url "follow" %}?next={{request.path}}" method="POST">
            <input type="hidden" name="object" value="{{follow_code}}">
            <input type="hidden" name="message" value="You are now following {{event.name}} discussion">
            <button type="submit">Follow</button>
        </form>

**Unfollowing**

To unfollow an object, use the ``unfollow`` method of the User instance::
    
    user.unfollow(event, "discuss",)

alternatively, a view has been set up which can be pushed to and will deal with these unfollows. To use this first call ``follow_object_code`` on the User instance to generate a signed code (this ensures that users can only set up follows which are authorised)::

    code = user.follow_object_code(event, "discuss")

Then allow the user to POST this code to the "unfollow" view (as the "object" parameter). You should also pass a "next" GET parameter which tells the view where to redirect to, and the "message" parameter which will be sent as success :ref:`dev_flash_messages`..::
    
        <form action="{% url "unfollow" %}?next={{request.path}}" method="POST">
            <input type="hidden" name="object" value="{{follow_code}}">
            <input type="hidden" name="message" value="You are no longer following {{event.name}} discussion">
            <button type="submit">Unfollow</button>
        </form>

**Sending notifications**

To send notifications to followers use the ``happening.notifications.notify_following`` method::
    
    notify_following(
            event, "discuss", CommentNotification,
            {"comment": comment,
             "author_photo_url": comment.author.profile.photo_url(),
             "author_name": str(comment.author),
             "object_name": str(event),
             "object_url": request.POST['next']},
            ignore=[request.user])

The ``ignore`` parameter indicates a list of users who should not recieve the notification, even if they are following. In this example it includes the user who is making the comment.