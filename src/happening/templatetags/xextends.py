"""Allow parameters when extending.

Based on https://djangosnippets.org/snippets/447/. Modified for use
with variables.
"""

from django import template
from django.template.loader_tags import do_extends
import tokenize
import io

register = template.Library()


class XExtendsNode(template.Node):

    """Allow parameters when extending."""

    def __init__(self, node, kwargs):
        """Allow parameters when extending."""
        self.node = node
        self.kwargs = kwargs

    def render(self, context):
        """Allow parameters when extending."""
        for k in list(self.kwargs.keys()):
            self.kwargs[k] = self.kwargs[k].resolve(context)
        context.update(self.kwargs)
        try:
            return self.node.render(context)
        finally:
            context.pop()


def do_xextends(parser, token):
    """Allow parameters when extending."""
    bits = token.contents.split()
    kwargs = {}
    if 'with' in bits:
        pos = bits.index('with')
        argslist = bits[pos+1:]
        bits = bits[:pos]
        for i in argslist:
            try:
                a, b = i.split('=', 1)
                a = a.strip()
                b = b.strip()

                keys = list(
                    tokenize.generate_tokens(io.StringIO(a).readline))
                if keys[0][0] == tokenize.NAME:
                    kwargs[str(a)] = template.Variable(b)
                else:
                    raise ValueError
            except ValueError:
                raise template.TemplateSyntaxError
        token.contents = " ".join(bits)

    # let the orginal do_extends parse the tag, and wrap the ExtendsNode
    return XExtendsNode(do_extends(parser, token), kwargs)

register.tag('xextends', do_xextends)
