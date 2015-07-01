"""Appearance helpers."""
import sass
import os
from uuid import uuid4
from django.contrib.sites.models import Site


def generate_css(variables=None):
    """Generate CSS according to variables provided."""
    if not variables:
        site = Site.objects.first().happening_site
        variables = {"THEME-COLOUR": site.theme_colour,
                     "PRIMARY-COLOUR": site.primary_colour}

    uid = uuid4().hex
    target = open("static/sass/%s.scss" % uid, 'w')
    try:
        for k, v in variables.items():
            target.write("$%s: %s;\n" % (k, v))
        target.write('@import "main.scss";')
        target.close()

        compiled = sass.compile(filename="static/sass/%s.scss" % uid)
    finally:
        os.remove("static/sass/%s.scss" % uid)

    return compiled
