Groups
=======

The groups plugin allows for events where attendees are separated into groups. These groups can be assigned by organisers, self-assigned by attendees, or generated randomly. If the groups are generated randomly they can take into account attributes of the attendees to balance groups (for example, to ensure that groups are mixed-skillset or mixed-ability).

**Group Permissions**

When creating an event, you are asked to assign the permissions of attendees to create, move, and modify groups.

Creation refers to creating and joining a new group, moving involves joining or leaving existing groups, and modifying groups allows attendees to edit the named and properties of the group they are in.

The options for permission levels are:

* Attendees cannot create/move/edit groups
* Attendees can create/move/edit groups after the event starts
* Attendees can create/move/edit groups at any time
* Attendees can create/move/edit groups after they are checked in

These rules do not apply to staff members who are always able to create, move, and edit groups.

**Group Properties**

When creating an event, you are able to specify a number of properties which attendees will be attached to groups. These properties appear one the create group form and the edit group form and can be set by staff, or by attendees who are members of the group.

The properties can be:

* Text, which is a single line text input
* Email, which is a valid email address
* Number, which is an integer
* URL, which is a valid URL
* Boolean, which is a checkbox indicating True or False

**Creating Groups**

Groups can be created by viewing the event and clicking ``Add a group``. You will be asked for the ``Team name``, ``Description``, and any custom group properties configured for the event. After clicking ``Save`` the group will be created and you will join it by default.

**Joining Groups**

If you are not a member of a group, and have permission to move groups, visiting the event page will show ``join group`` alongside each group. Clicking this will add you to the group.

**Leaving Groups**

If you are a member of a group, and have permission to move groups, visiting the event page will show ``leave group`` alongside the group you are part of. Clicking this will remove you from the group.

**Staff Moving Groups**

Staff can move attendees around groups by visiting the event page in the Staff panel, and clicking the edit icon (a pencil) alongside an attendee's name.

**Generating Groups**

To generate a group, visit the event page in the Staff panel and click ``Generate Groups``. You then decide if you wish to clear existing groups, if only checked-in attendees should be grouped, and how many groups you want to create. Attendees will be split evenly between the groups.

**Viewing Groups**

Clicking ``View Groups`` on the event page in the Staff panel will show all groups with avatars and names for members. This can be used when showing attendees which groups they are in.


**Event Configuration**

.. automodule:: plugins.groups.event_configuration
   :members:
   :undoc-members:
   :noindex: