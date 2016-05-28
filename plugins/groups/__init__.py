"""Split members into groups, with automatic/manual grouping."""
import copy


class Plugin(object):

    """Split members into groups, with automatic/manual grouping."""

    name = "Groups"
    url_root = "groups/"
    staff_url_root = "groups/"


def generate_groups(ungrouped_users, number_of_groups, existing_groups=None):
    """Generate groups maintaining existing groups.

    ungrouped_users is a list of users who have not been placed in groups

    number_of_groups is an int

    existing_groups is a dictionary with the group number as the key, and
    the content is a list of members of that group. Group numbers start from 0.

    Returns a list of lists, each list is a group. Group numbers start from 0.
    """
    ungrouped_users = copy.copy(ungrouped_users)

    if not existing_groups:
        existing_groups = {}

    number_of_attendees = len(ungrouped_users) + len(
        sum(list(existing_groups.values()), []))

    # Create an in-memory model of the groups
    groups = [[] for group in range(min([number_of_groups,
                                         number_of_attendees]))]

    # Assigned existing groups
    for k, v in list(existing_groups.items()):
        groups[k] = v

    # Assign unassigned members to the groups
    while len(ungrouped_users) > 0:
        # Figure out which index has the smallest number of people and add
        smallest_index = sorted(
            enumerate(groups), key=lambda v: len(v[1]))[0][0]
        groups[smallest_index].append(ungrouped_users.pop())

    return groups
