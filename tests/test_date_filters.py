from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from tests.factories import EventFactory
from wagtail_events import date_filters
from wagtail_events.models import Event


class TestAgendas(TestCase):
    """Tests for the get_*_agenda methods."""
    def setUp(self):
        self.now = timezone.now()
        self.detail = EventFactory.create(
            parent=None,
            start_date=self.now
        )

    # def test_get_year_agenda(self):
    #     """Test get_year_agenda returns the expected data."""
    #     instance_two = EventFactory.create(
    #         event_series=self.detail,
    #         start_date=self.now-timedelta(days=365),
    #     )
    #     response = date_filters.get_year_agenda(
    #         Event,
    #         Event.objects.all(),
    #         self.now,
    #     )
    #     print('HERE')
    #     print(response.json())
    #
    #     self.assertEqual(response['scope'], 'Year')
    #     self.assertIn(self.instance_one, response['items'])
    #     self.assertNotIn(instance_two, response['items'])

    # def test_get_month_agenda(self):
    #     """Test get_month_agenda returns the expected data."""
    #     instance_two = EventFactory.create(
    #         event_series=self.detail,
    #         start_date=self.now-timedelta(weeks=4),
    #     )
    #     response = date_filters.get_month_agenda(
    #         SubEvent,
    #         EventSeries.objects.all(),
    #         self.now,
    #     )
    #
    #     self.assertEqual(response['scope'], 'Month')
    #     self.assertIn(self.instance_one, response['items'])
    #     self.assertNotIn(instance_two, response['items'])
    #
    # def test_get_week_agenda(self):
    #     """Test get_week_agenda returns the expected data."""
    #     instance_two = SubEventFactory.create(
    #         event_series=self.detail,
    #         start_date=self.now-timedelta(weeks=1),
    #     )
    #     response = date_filters.get_week_agenda(
    #         SubEvent,
    #         EventSeries.objects.all(),
    #         self.now,
    #     )
    #
    #     self.assertEqual(response['scope'], 'Week')
    #     self.assertIn(self.instance_one, response['items'])
    #     self.assertNotIn(instance_two, response['items'])
    #
    # def test_get_day_agenda(self):
    #     """Test get_day_agenda returns the expected data."""
    #     instance_two = SubEventFactory.create(
    #         event_series=self.detail,
    #         start_date=self.now-timedelta(days=1),
    #     )
    #     response = date_filters.get_day_agenda(
    #         SubEvent,
    #         EventSeries.objects.all(),
    #         self.now,
    #     )
    #
    #     self.assertEqual(response['scope'], 'Day')
    #     self.assertIn(self.instance_one, response['items'])
    #     self.assertNotIn(instance_two, response['items'])
