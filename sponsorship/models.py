""" Sponsorship models. """
from django.db import models


class Sponsor(models.Model):

    """ A Sponsor of an individual event. """

    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    logo = models.ImageField(upload_to="sponsors")

    def __unicode__(self):
        return self.name
