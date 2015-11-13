"""Test event model."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from happening.utils import custom_strftime


class TestEvent(TestCase):

    """Test event model."""

    def setUp(self):
        """Just get today's day."""
        super(TestEvent, self).setUp()
        self.today_day = datetime.now(pytz.utc).weekday()

    def test_is_future(self):
        """Test that is_future works."""
        past_event = mommy.prepare("Event", start=datetime.now(pytz.utc) -
                                   timedelta(days=20))
        self.assertFalse(past_event.is_future)
        future_event = mommy.prepare("Event", start=datetime.now(pytz.utc) +
                                     timedelta(days=20))
        self.assertTrue(future_event.is_future)

    def test_humanize_1(self):
        """Test that time_to_string humanizes correctly 1."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=MO))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 0:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 6:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Monday (%s) at 7PM" % e)

    def test_humanize_2(self):
        """Test that time_to_string humanizes correctly 2."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=TU))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 1:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 0:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Tuesday (%s) at 7PM" % e)

    def test_humanize_3(self):
        """Test that time_to_string humanizes correctly 3."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=WE))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 2:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 1:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Wednesday (%s) at 7PM" % e)

    def test_humanize_4(self):
        """Test that time_to_string humanizes correctly 4."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=TH))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 3:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 2:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Thursday (%s) at 7PM" % e)

    def test_humanize_5(self):
        """Test that time_to_string humanizes correctly 5."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=FR))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 4:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 3:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Friday (%s) at 7PM" % e)

    def test_humanize_6(self):
        """Test that time_to_string humanizes correctly 6."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=SA))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 5:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 4:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Saturday (%s) at 7PM" % e)

    def test_humanize_7(self):
        """Test that time_to_string humanizes correctly 7."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=SU))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 6:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 5:
            self.assertEquals(event.time_to_string, "tomorrow (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "next Sunday (%s) at 7PM" % e)

    def test_humanize_8(self):
        """Test that time_to_string humanizes correctly 8."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=MO(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 0:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 1:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Monday (%s) at 7PM" % e)

    def test_humanize_9(self):
        """Test that time_to_string humanizes correctly 9."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=TU(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 1:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 2:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Tuesday (%s) at 7PM" % e)

    def test_humanize_10(self):
        """Test that time_to_string humanizes correctly 10."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=WE(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 2:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 3:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Wednesday (%s) at 7PM" % e)

    def test_humanize_11(self):
        """Test that time_to_string humanizes correctly 11."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=TH(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 3:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 4:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Thursday (%s) at 7PM" % e)

    def test_humanize_12(self):
        """Test that time_to_string humanizes correctly 12."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=FR(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 4:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 5:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Friday (%s) at 7PM" % e)

    def test_humanize_13(self):
        """Test that time_to_string humanizes correctly 13."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=SA(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 5:
            self.assertEquals(event.time_to_string, "today (%s) at 7PM" % e)
        elif self.today_day == 6:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Saturday (%s) at 7PM" % e)

    def test_humanize_14(self):
        """Test that time_to_string humanizes correctly 14."""
        event = mommy.prepare("Event", start=datetime.now(pytz.utc).replace(
            hour=19, minute=0) + relativedelta(weekday=SU(-1)))
        e = custom_strftime("{S}", event.start)
        if self.today_day == 6:
            self.assertEquals(event.time_to_string,
                              "today (%s) at 7PM" % e)
        elif self.today_day == 0:
            self.assertEquals(event.time_to_string,
                              "yesterday (%s) at 7PM" % e)
        else:
            self.assertEquals(event.time_to_string,
                              "last Sunday (%s) at 7PM" % e)

        event = mommy.prepare("Event", start=datetime(2011, 01, 01))
        self.assertEquals(event.time_to_string,
                          "Saturday January 1st, 2011 at 12AM")

        event = mommy.prepare("Event", start=datetime(2011, 01, 01, 7, 30))
        self.assertEquals(event.time_to_string,
                          "Saturday January 1st, 2011 at 7:30AM")

    def test_previous_event(self):
        """Test that previous event returns correctly."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) -
                           timedelta(days=2))

        self.assertEquals(event.previous_event, None)

        event2 = mommy.make("Event", start=datetime.now(pytz.utc) -
                            timedelta(days=4))

        self.assertEquals(event.previous_event, event2)

        mommy.make("Event", start=datetime.now(pytz.utc) -
                   timedelta(days=6))

        self.assertEquals(event.previous_event, event2)
