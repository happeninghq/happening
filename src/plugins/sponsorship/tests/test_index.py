"""Test sponsor on index."""

# from happening.tests import TestCase
# from model_mommy import mommy
# from datetime import datetime, timedelta
# import pytz


# class TestIndex(TestCase):

#     """Test sponsor on index."""

#     def test_index_no_events(self):
#         """Test it hides there are no events."""
#         response = self.client.get("/")
#         self.assertIsNone(response.soup.find(id="sponsors"))

#     def test_index_no_sponsor(self):
#         """Test it hides the event has no sponsor."""
#         mommy.make("Event")
#         response = self.client.get("/")
#         self.assertIsNone(response.soup.find(id="sponsors"))

#     def test_index_future_sponsor(self):
#         """Test it displays correctly when a future event has a sponsor."""
#         mommy.make("Event", start=datetime.now(pytz.utc) +
#                    timedelta(days=20), sponsor=mommy.make("Sponsor"))
#         response = self.client.get("/")
#         sponsor_info = response.soup.find(id="sponsors")
#         self.assertIsNotNone(sponsor_info)
#         self.assertTrue("is kindly" in sponsor_info.text)
#         self.assertFalse("was kindly" in sponsor_info.text)

#     def test_index_past_sponsor(self):
#         """Test it displays correctly when a past event has a sponsor."""
#         mommy.make("Event", start=datetime.now(pytz.utc) -
#                    timedelta(days=20), sponsor=mommy.make("Sponsor"))
#         response = self.client.get("/")
#         sponsor_info = response.soup.find(id="sponsors")
#         self.assertIsNotNone(sponsor_info)
#         self.assertTrue("was kindly" in sponsor_info.text)
#         self.assertFalse("is kindly" in sponsor_info.text)
