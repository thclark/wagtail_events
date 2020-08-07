# -*- coding:utf8 -*-

from __future__ import unicode_literals

from django.test import RequestFactory, TestCase
from django.utils import timezone
from wagtail_events.templatetags import wagtail_events_tags


class TestQueryString(TestCase):
    """Tests for the querystring template tag."""

    def test_no_querystring(self):
        """Test the querystring handles no input."""
        request = RequestFactory().get("")
        context = {"request": request}
        response = wagtail_events_tags.querystring(context)

        self.assertEqual(response, "")

    def test_querystring_existing(self):
        """Test querystring method handles existing querystrings."""
        request = RequestFactory().get("", {"page": "1"})
        context = {"request": request}
        response = wagtail_events_tags.querystring(context, scope="year")

        self.assertIn("scope=year", response)
        self.assertIn("&", response)
        self.assertIn("page=1", response)

    def test_querystring(self):
        """Test querystring method overwrites existing matching querystrings."""
        request = RequestFactory().get("", {"scope": "day"})
        context = {"request": request}
        response = wagtail_events_tags.querystring(context, "scope", scope="year")

        self.assertEqual(response, "scope=year")


class TestPatch(TestCase):
    """Tests for the _patch template tags."""

    def setUp(self):
        request = RequestFactory().get("")
        self.context = {"request": request}

    def test_patch(self):
        """Test _patch retuns the correct data."""
        response = wagtail_events_tags._patch(self.context, "foo", "bar")

        self.assertEqual(response, "?foo=bar")

    def test_patch_scope(self):
        """Test patch_scope retuns the correct data with scope."""
        response = wagtail_events_tags.patch_scope(self.context, "foo")

        self.assertEqual(response, "?scope=foo")

    def test_patch_start_date(self):
        """Test patch_start_date retuns the correct data with start_date."""
        time = timezone.now()
        response = wagtail_events_tags.patch_start_date(self.context, time)

        self.assertEqual(
            response, "?start_date={}".format(time.strftime("%Y.%m.%d")),
        )
