Filtering
==============

The Happening Filtering Language will be used throughout happening to allow staff members to target members. Currently it is only used as a target for :ref:`emails`, but in the future it will be used to specify ticket eligibility, voting eligibility, group membership, etc.

The Happening Filter Language maps directly to Django queries. Differences are that keys and values are separated by ``:`` instead of ``=``, ``count`` being annotated automatically, and the addition of the ``has`` keyword. To access attributes of related models you still use __.

**Count**

To filter users who have at least one ticket, use ``tickets__count__gt:0``. There is currently no way of counting the result of a previous query.

**Has**

Has is used to confirm that a relationship exists matching a subquery. For example ``tickets__has:(event__id:1 cancelled:True)`` will find every User who has a cancelled ticket for event 1.

**Select All**

To target every member of the system, a blank query will suffice.

**Tickets to a particular event**

As shown above, ``tickets__has:(event__id:1 cancelled:False)`` will find all members who have active tickets to a Event 1.

**A specific Member**

Members can be targetted using simple key querying. E.g. ``id:1``
