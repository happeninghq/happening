"""Test helper functionality."""
from django_bs_test import TestCase as bsTestCase
from django_bs_test import Client
import vcr
import os
from model_mommy import mommy
from django.contrib.sites.models import Site
import collections


def add_site_to_all_models(*args, **kwargs):
    """Add the site to all models."""
    try:
        if 'site' not in kwargs:
            kwargs['site'] = Site.objects.first()
        return mommy._make(*args, **kwargs)
    except TypeError:
        del kwargs['site']
        return mommy._make(*args, **kwargs)

mommy._make = mommy.make
mommy.make = add_site_to_all_models


class VCRPyAllMeta(type):

    """Add VCRPy to all methods."""

    def __new__(cls, name, bases, local):
        """When an instance is created set up the decorator."""
        for attr in local:
            value = local[attr]
            if isinstance(value, collections.Callable):
                local[attr] = vcr.use_cassette(
                    'vcr.yaml', record_mode='new_episodes')(value)
        return type.__new__(cls, name, bases, local)


class TestCase(bsTestCase, metaclass=VCRPyAllMeta):

    """Test case which includes beautifulsoup and http mocking."""

    def create_client(self):
        """Create a test client."""
        return Client()

if 'travis' in os.environ:
    # We don't use VCRPy on the CI server
    # (for some reason it doesn't work anyway...)
    TestCase = bsTestCase  # NOQA
