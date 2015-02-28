""" Page models. """
from django.db import models


class PageManager(models.Manager):

    """ Custom Page Manager. """

    def as_navigation_path(self):
        """ Return a dict of "directories" and links.

        e.g.

        {
            "About": {
                "About": "about",
                "Sponsorship": "sponsorship"
            },
            "A Third Page": "anotherpage"
        }

        would mean there should be a container named "About" which contains two
        links, the "About" link which links to the "about" page, and the
        "Sponsorship" link which links to the "sponsorship" page. After the
        "About" container there is a link "A Third Page" which links to the
        "anotherpage" page.
        """

        def add_path(level, path, page):
            if len(path) == 1:
                level[path[0]] = page.url
            else:
                if not path[0] in level:
                    level[path[0]] = {}
                add_path(level[path[0]], path[1:], page)

        first_level = {}
        for page in self.all():
            if page.path:
                add_path(first_level, page.path.split("/"), page)

        # TODO: Remove this when index is running from pages
        first_level["Home"] = ""

        return first_level


class Page(models.Model):

    """ A static page. """

    objects = PageManager()

    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    path = models.CharField(max_length=255, null=True)
    # path is a slash separated direction to the link as it appears in
    # primary navigation - if it is null then the page will not appear
    # in primary navigation
