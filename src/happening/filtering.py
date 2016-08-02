"""Filtering."""
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Count
from happening.utils import get_request
import re
from email.utils import parseaddr


class EmailUser(object):
    """A result when targeting an email address."""

    def __init__(self, email):
        """Create EmailUser."""
        self.email = email

    def __str__(self):
        """Return email."""
        return self.email


def split_attributes(str):
    """Split a HQL query into attributes."""
    attributes = []
    num_parenthesis = 0
    current_attribute = ""
    for s in str:
        if s == " " and num_parenthesis == 0:
            if current_attribute:
                attributes.append(current_attribute)
            current_attribute = ""
        else:
            current_attribute += s
            if s == "(":
                num_parenthesis += 1
            elif s == ")":
                num_parenthesis -= 1
    if current_attribute:
        attributes.append(current_attribute)
    return attributes


def query(str, data_type=User):
    """Get the results of a HQL Query."""
    # First we split by comma and use that to separate the component parts
    queries = str.split(",")
    if len(queries) > 1:
        return sum([list(query(s, data_type)) for s in queries], [])

    # First check if we have been given an email address
    email_address = parseaddr(str)[1]
    if '@' in email_address:
        # We have an email address
        # First, check if there is a user that matches the email address
        user = data_type.objects.filter(email=email_address).first()
        if user is None:
            # No user, create a temporary one
            return [EmailUser(email_address)]
        return [user]

    attributes = split_attributes(str)

    q = data_type.objects.all()

    for attribute in attributes:
        key, value = attribute.split(":", 1)

        key_parts = key.split("__")
        if len(key_parts) > 1:
            if key_parts[1] == 'count':
                q = q.annotate(Count(key_parts[0]))
            if key_parts[1] == 'has':
                # We now pull out everything in the brackets
                # and evaluate that

                # This only works if the "has" is on the "many" side of the
                # relationship. TODO: If needed, add one for the "one" side.
                related_model = data_type._meta.get_field(
                    key_parts[0]).field.model
                results = query(value[1:-1], related_model)

                q = q.filter(**{key_parts[0] + "__in": results})
                continue

        # Now check if we need to coerce the type of value. For example
        # If value is "True" or "False" (regardless of case) and the datatype
        # of key is Boolean then we convert it to boolean
        if value.lower() in ['true', 'false']:
            key_type = data_type._meta.get_field(key)
            if key_type.__class__.__name__ == "BooleanField":
                value = value.lower() == 'true'
        q = q.filter(**{key: value})

    return q


def matches(obj, query_str):
    """A query matches a given object."""
    if obj.__class__ == AnonymousUser:
        # This is a special case - where we'll fake the filtering
        # for now we'll only allow filtering by tag
        result = re.match("tags__has:\(tag:(.*)\)", query_str)
        if result:
            tag = result.groups()[0]
            return tag in get_request().session.get('tags', [])
        return False
    return obj in query(query_str, obj.__class__)
