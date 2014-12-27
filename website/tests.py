""" Test helper functionality. """
from django_bs_test import TestCase as bsTestCase
import vcr
import os


class VCRPyAllMeta(type):

    """ Add VCRPy to all methods. """

    def __new__(cls, name, bases, local):
        """ When an instance is created set up the decorator. """
        for attr in local:
            value = local[attr]
            if callable(value):
                local[attr] = vcr.use_cassette(
                    'vcr.yaml', record_mode='new_episodes')(value)
        return type.__new__(cls, name, bases, local)


class TestCase(bsTestCase):

    """ Test case which includes beautifulsoup and http mocking. """

    __metaclass__ = VCRPyAllMeta

if 'travis' in os.environ:
    # We don't use VCRPy on the CI server
    # (for some reason it doesn't work anyway...)
    TestCase = bsTestCase  # NOQA
