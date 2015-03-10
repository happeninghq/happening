""" Custom happening database manipulation. """

from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.contrib.sites.models import Site
from multihost import sites
import os


class Manager(CurrentSiteManager):

    """ Override site manager to use hostname instead of settings. """

    def get_queryset(self):
        """ Get the current site ID from the URL. """
        site_id = 1

        if 'scdtest' not in os.environ and 'travis' not in os.environ:
            site = sites.by_host()
            if site:
                site_id = site.id

        return super(CurrentSiteManager, self).get_queryset().filter(
            **{self._get_field_name() + '__id': site_id})


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
            self.site = Site.objects.get(pk=1)
        else:
            self.site = sites.by_host()
        return super(Model, self).save(*args, **kwargs)
