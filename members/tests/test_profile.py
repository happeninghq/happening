""" Test viewing and editing profile. """

from django_bs_test import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from events.models import Ticket
from django.contrib.auth.models import User
from model_mommy.generators import gen_image_field
from django.conf import settings
import os.path


class TestProfile(TestCase):

    """ Test viewing and editing profile. """

    def setUp(self):
        """ Set up a user. """
        self.user = mommy.make("auth.User")
        self.user.set_password("password")
        self.user.save()

    def test_nonexisting_user_404s(self):
        """ Test that a nonexisting profile returns a 404. """
        response = self.client.get("/member/999", follow=True)
        self.assertEquals(404, response.status_code)

    def test_can_view_profile(self):
        """ Test that we can view an existing profile. """
        response = self.client.get("/member/%s" % self.user.id)
        self.assertTrue(str(self.user.profile) in response.content)
        self.assertTrue(str(self.user.profile.bio) in response.content)

    def test_cannot_edit_other_profiles(self):
        """ Test that users cannot edit other people's profiles. """
        user2 = mommy.make("auth.User")
        user2.set_password("password")
        user2.save()

        # First check logged out user can't edit profiles
        for url in ["/member/%s/edit", "/member/%s/edit/photo/crop"]:
            response = self.client.get(url % self.user.id, follow=True)
            self.assertTrue("accounts/login" in response.redirect_chain[0][0])
        response = self.client.post("/member/%s/edit/photo" % self.user.id,
                                    follow=True)
        self.assertTrue("accounts/login" in response.redirect_chain[0][0])

        # Then check that logged in users can't edit other user's profiles
        self.client.login(username=user2.username, password="password")
        for url in ["/member/%s/edit", "/member/%s/edit/photo/crop"]:
            response = self.client.get(url % self.user.id)
            self.assertEquals(404, response.status_code)
        response = self.client.post("/member/%s/edit/photo" % self.user.id,
                                    follow=True)
        self.assertEquals(404, response.status_code)

    def test_can_edit_profile_fields(self):
        """ Test a user can edit their own text profile fields. """
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/member/%s/edit" % self.user.id)
        self.assertEquals(200, response.status_code)

        response = self.client.post("/member/%s/edit" % self.user.id,
                                    {"first_name": "j",
                                     "last_name": "s",
                                     "bio": "test 1 2 3"}, follow=True)
        self.assertTrue(
            "/member/%s" % self.user.id in response.redirect_chain[0][0])

        self.user = User.objects.get(pk=self.user.id)
        self.assertEquals("j", self.user.first_name)
        self.assertEquals("s", self.user.last_name)
        self.assertEquals("test 1 2 3", self.user.profile.bio)

    def test_can_upload_photo(self):
        """ Test that an image can be uploaded. """
        self.client.login(username=self.user.username, password="password")
        f = gen_image_field()
        response = self.client.post('/member/%s/edit/photo' % self.user.id,
                                    {'photo': f}, follow=True)
        self.assertTrue("/member/%s/edit/photo/crop" % self.user.id
                        in response.redirect_chain[0][0])
        self.user = User.objects.get(pk=self.user.id)
        self.assertFalse("dojo-logo" in self.user.profile.photo_url())

        # Check that when overwriting image, the original image is deleted
        filepath = "%s/%s" % (settings.MEDIA_ROOT, self.user.profile.photo)
        self.assertTrue(os.path.isfile(filepath))
        f = gen_image_field()
        f.name = "test-123.jpg"

        response = self.client.post('/member/%s/edit/photo' % self.user.id,
                                    {'photo': f}, follow=True)
        self.assertTrue("/member/%s/edit/photo/crop" % self.user.id
                        in response.redirect_chain[0][0])
        self.user = User.objects.get(pk=self.user.id)
        filepath2 = "%s/%s" % (settings.MEDIA_ROOT, self.user.profile.photo)

        self.assertNotEqual(filepath, filepath2)
        self.assertFalse(os.path.isfile(filepath))

    def test_default_photo(self):
        """ Test that default photos are correct. Including gravatar. """
        # Test without gravatar
        self.assertTrue("dojo-logo" in self.user.profile.photo_url())

        # Test with gravatar
        self.user.email = "jonathan@jscott.me"
        self.user.save()

        self.assertTrue("gravatar" in self.user.profile.photo_url())

    def test_resize_crop_photo(self):
        """ Test resizing and cropping a photo. """
        pass # TODO
