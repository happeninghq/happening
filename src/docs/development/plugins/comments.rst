.. _dev_plugins_comments:

Comments
=============

To include comments on a page add::
    
    {% comments object %}

where object is the object you wish to attach the discussion to. When posting a comment users will automatically follow the "discuss" role of object. To allow people to optionally follow/unfollow a discussion, see :ref:`dev_following`.