"""Template tags relating to permissions."""

from django.template import Library, Node, TemplateSyntaxError
from django.urls import reverse, resolve
register = Library()


@register.tag
def linkpermission(parser, token):
    """Allow custom content when permission is enabled for a given link."""
    try:
        tag, test = token.contents.split()
    except (ValueError, TypeError):
        raise TemplateSyntaxError(
            "'%s' tag takes two parameters" % tag)

    default_states = ['linkpermission', 'else']
    end_tag = 'endlinkpermission'

    # Place to store the states and their values
    states = {}

    # Let's iterate over our context and find our tokens
    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()

    linkpermission_name = parser.compile_filter(test)
    return LinkPermissionNode(states, linkpermission_name)


class LinkPermissionNode(Node):
    """Allow custom content when permission is enabled for a given link."""

    def __init__(self, states, linkpermission_name):
        """Allow custom content when permission is enabled for a given link."""
        self.states = states
        self.linkpermission_name = linkpermission_name

    def render(self, context):
        """Allow custom content when permission is enabled for a given link."""
        # Resolving variables passed by the user
        linkpermission_name = self.linkpermission_name.resolve(context, True)
        path = reverse(linkpermission_name)  # TODO, kwargs=kwargs)
        view = resolve(path).func

        if not(hasattr(view, "has_permission")) or\
                view.has_permission(context["user"]):
            return self.states['linkpermission'].render(context)
        return ""
