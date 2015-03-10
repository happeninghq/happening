""" Test viewing and editing profile. """

from happening.tests import TestCase
from model_mommy import mommy
from django.contrib.auth import get_user_model
from model_mommy.generators import gen_image_field
from django.conf import settings
import os.path
from StringIO import StringIO
from PIL import Image


class TestProfile(TestCase):

    """ Test viewing and editing profile. """

    def setUp(self):
        """ Set up a user. """
        self.user = mommy.make(settings.AUTH_USER_MODEL)
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
        user2 = mommy.make(settings.AUTH_USER_MODEL)
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

        self.user = get_user_model().objects.get(pk=self.user.id)
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
        self.user = get_user_model().objects.get(pk=self.user.id)
        self.assertIsNotNone(self.user.profile.photo)

        # Check that when overwriting image, the original image is deleted
        filepath = "%s/%s" % (settings.MEDIA_ROOT, self.user.profile.photo)
        self.assertTrue(os.path.isfile(filepath))
        f = gen_image_field()
        f.name = "test-123.jpg"

        response = self.client.post('/member/%s/edit/photo' % self.user.id,
                                    {'photo': f}, follow=True)
        self.assertTrue("/member/%s/edit/photo/crop" % self.user.id
                        in response.redirect_chain[0][0])
        self.user = get_user_model().objects.get(pk=self.user.id)
        filepath2 = "%s/%s" % (settings.MEDIA_ROOT, self.user.profile.photo)

        self.assertNotEqual(filepath, filepath2)
        self.assertFalse(os.path.isfile(filepath))

    def test_default_photo(self):
        """ Test that default photos are correct."""
        self.assertTrue("gravatar" in self.user.profile.photo_url())

    def test_resize_crop_photo(self):
        """ Test resizing and cropping a photo. """
        self.client.login(username=self.user.username, password="password")
        # Upload the image
        f = gen_image_field()

        imagedata = StringIO(f.read())
        f.seek(0)
        image = Image.open(imagedata)

        X1 = 10
        X2 = 30
        Y1 = 10
        Y2 = 30

        top_left_pixel = image.getpixel((X1, Y1))

        response = self.client.post('/member/%s/edit/photo' % self.user.id,
                                    {'photo': f}, follow=True)

        self.user = get_user_model().objects.get(pk=self.user.id)

        # Now we post the crop

        response = self.client.post(
            '/member/%s/edit/photo/crop' % self.user.id,
            {'x1': X1, 'y1': Y1, 'x2': X2, 'y2': Y2}, follow=True)
        self.assertTrue(
            "/member/%s" % self.user.id in response.redirect_chain[0][0])

        self.user = get_user_model().objects.get(pk=self.user.id)
        imagedata = StringIO(self.user.profile.photo.read())
        image = Image.open(imagedata)
        self.assertEqual((X2-X1, Y2-Y1), image.size)

        self.assertEqual(top_left_pixel, image.getpixel((0, 0)))
