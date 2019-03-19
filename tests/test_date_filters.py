# -*- coding:utf8 -*-

from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from tests.factories import EventDetailFactory, EventOccurrenceFactory
from wagtail_events import date_filters
from wagtail_events.models import EventDetail, EventOccurrence


class TestAgendas(TestCase):
    """Tests for the get_*_agenda methods."""
    def setUp(self):
        self.now = timezone.now()
        self.detail = EventDetailFactory.create(parent=None)
        self.instance_one = EventOccurrenceFactory.create(
            event=self.detail,
            start_date=self.now,
        )

    def test_get_year_agenda(self):
        """Test get_year_agenda returns the expected data."""
        instance_two = EventOccurrenceFactory.create(
            event=self.detail,
            start_date=self.now-timedelta(days=365),
        )
        response = date_filters.get_year_agenda(
            EventOccurrence,
            EventDetail.objects.all(),
            self.now,
        )

        self.assertEqual(response['scope'], 'Year')
        self.assertIn(self.instance_one, response['items'])
        self.assertNotIn(instance_two, response['items'])

    def test_get_month_agenda(self):
        """Test get_month_agenda returns the expected data."""
        instance_two = EventOccurrenceFactory.create(
            event=self.detail,
            start_date=self.now-timedelta(weeks=4),
        )
        response = date_filters.get_month_agenda(
            EventOccurrence,
            EventDetail.objects.all(),
            self.now,
        )

        self.assertEqual(response['scope'], 'Month')
        self.assertIn(self.instance_one, response['items'])
        self.assertNotIn(instance_two, response['items'])

    def test_get_week_agenda(self):
        """Test get_week_agenda returns the expected data."""
        instance_two = EventOccurrenceFactory.create(
            event=self.detail,
            start_date=self.now-timedelta(weeks=1),
        )
        response = date_filters.get_week_agenda(
            EventOccurrence,
            EventDetail.objects.all(),
            self.now,
        )

        self.assertEqual(response['scope'], 'Week')
        self.assertIn(self.instance_one, response['items'])
        self.assertNotIn(instance_two, response['items'])

    def test_get_day_agenda(self):
        """Test get_day_agenda returns the expected data."""
        instance_two = EventOccurrenceFactory.create(
            event=self.detail,
            start_date=self.now-timedelta(days=1),
        )
        response = date_filters.get_day_agenda(
            EventOccurrence,
            EventDetail.objects.all(),
            self.now,
        )

        self.assertEqual(response['scope'], 'Day')
        self.assertIn(self.instance_one, response['items'])
        self.assertNotIn(instance_two, response['items'])
