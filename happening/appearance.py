"""Appearance helpers."""
import sass
import os
from uuid import uuid4
from django.contrib.sites.models import Site


def generate_css(variables=None):
    """Generate CSS according to variables provided."""
    if not variables:
        site = Site.objects.first().happening_site
        variables = site.theme_settings

        # Now also load settings file
        with open("static/sass/settings.scss") as f:
            settings = parse_settings(f.read())
            for category in settings:
                for setting, value in settings[category].items():
                    if setting not in variables:
                        variables[setting] = value

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


def parse_settings(content):
    """Parse a settings.scss file."""
    categories = {}

    mode = "None"
    current_category = ""

    for line in content.strip().split("\n"):
        l = line.strip('* ')

        if mode == "None":
            if l == "/":
                mode = "Comment"
                current_category = ""
            elif l.startswith("$"):
                # Adding a variable
                line_parts = [p.strip(" ;") for p in l[1:].split(":")]
                categories[current_category][line_parts[0]] = line_parts[1]
        elif mode == "Comment":
            if l == "/":
                mode = "None"
                if current_category not in categories:
                    categories[current_category] = {}
            else:
                current_category += l

    return categories
