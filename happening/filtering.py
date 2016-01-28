"""Filtering."""
from django.contrib.auth.models import User
from django.db.models import Count


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
                related_model = data_type._meta.get_field_by_name(
                    key_parts[0])[0].field.model
                results = query(value[1:-1], related_model)

                q = q.filter(**{key_parts[0] + "__in": results})
                continue

        # Now check if we need to coerce the type of value. For example
        # If value is "True" or "False" (regardless of case) and the datatype
        # of key is Boolean then we convert it to boolean
        if value.lower() in ['true', 'false']:
            key_type = data_type._meta.get_field_by_name(key)[0]
            if key_type.__class__.__name__ == "BooleanField":
                value = value.lower() == 'true'
        q = q.filter(**{key: value})

    return q
