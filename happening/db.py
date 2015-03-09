""" Custom happening database manipulation. """

from django.contrib.sites.managers import CurrentSiteManager as Manager
from django.db import models
from django.contrib.sites.models import Site
from multihost import sites
import os


class Model(models.Model):

    """ Custom model for use in happening.

    Ensures that models are owned by a particular site.
    """

    class Meta:
        abstract = True

    site = models.ForeignKey(Site)
    objects = Manager()

    def save(self, *args, **kwargs):
        """ Ensure there is a site for this instance. """
        if 'scdtest' in os.environ or 'travis' in os.environ:
            self.site = Site.objects.first()
        else:
            self.site = sites.by_host()
        return super(Model, self).save(*args, **kwargs)
