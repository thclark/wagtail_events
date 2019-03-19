# -*- coding:utf8 -*-

from __future__ import unicode_literals

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.paginator import Page as PaginatorPage, Paginator
from django.test import RequestFactory, TestCase
from django.utils import timezone
from mock import patch, Mock
from modelcluster.fields import ParentalKey
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail_factories import SiteFactory

from tests import factories
from wagtail_events import abstract_models
from wagtail_events import models
from wagtail_events.views import EventOccurrenceDetailView
from wagtail_events.utils import _DATE_FORMAT_RE


class TestEventDetail(TestCase):
    """Tests for the EventDetail model."""
    def setUp(self):
        self.model = models.EventDetail

    def test_parent_class(self):
        """EventDetail should inhert from Page & RoutablePageMixin."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(self.model, RoutablePageMixin))

    def test_body(self):
        """Test the EventDetail.body field."""
        field = self.model._meta.get_field('body')

        self.assertIsInstance(field, RichTextField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_event_view(self):
        """Test EventDetail.event_view returns the expected data."""
        request = RequestFactory().get('')
        request.is_preview = False
        detail = factories.EventDetailFactory.create(parent=None)
        instance = factories.EventOccurrenceFactory.create(
            event=detail,
            start_date=timezone.now(),
        )
        response = detail.event_view(request, pk=instance.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], instance)
        self.assertIsInstance(
            response.context_data['view'],
            EventOccurrenceDetailView,
        )


class TestEventIndex(TestCase):
    """Tests for the EventIndex model."""
    def setUp(self):
        self.model = models.EventIndex
        self.index = factories.EventIndexFactory.create(
            parent=None,
            paginate_by=10
        )
        self.detail = factories.EventDetailFactory.create(
            parent=self.index,
            show_in_menus=True,
        )
        self.detail_2 = factories.EventDetailFactory.create(
            parent=self.index,
            show_in_menus=False,
        )
        self.instance = factories.EventOccurrenceFactory.create(
            event=self.detail,
            start_date=timezone.now(),
        )
        self.instance_2 = factories.EventOccurrenceFactory.create(
            event=self.detail_2,
            start_date=timezone.now(),
        )
        self.request = RequestFactory().get('')
        self.request.is_preview = False

    def test_parent_class(self):
        """EventIndex should inherit from AbstractEventIndex."""
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractEventIndex
        ))

    def test_body(self):
        """Test the EventIndex.body field."""
        field = self.model._meta.get_field('body')

        self.assertIsInstance(field, RichTextField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_get_children(self):
        """Test EventIndex._get_children returns the expected data."""
        response = self.index._get_children(self.request)

        self.assertEqual(response['items'][0], self.instance)

    def test_get_children_with_time(self):
        """
        Test EventIndex._get_children returns the expected data.
        When scope & start_date querystrings are provided the list of children
        will be filtered depending on scope from the startime.
        """
        request = RequestFactory().get('', {
            'scope': 'year',
            'start_date': timezone.now().strftime('%Y.01.01'),
        })
        request.is_preview = False
        response = self.index._get_children(request)

        self.assertEqual(response['items'][0], self.instance)

    def test_get_children_bad_time_period(self):
        """
        Test EventIndex._get_children returns default data when bad
        querystrings are provided.
        """
        request = RequestFactory().get('', {'scope': 'bad_scope'})
        request.is_preview = False
        response = self.index._get_children(request)

        self.assertEqual(response['items'][0], self.instance)

    def test_get_dateformat(self):
        """EventIndex.get_dateformat should return the correct date format."""
        response = self.index.get_dateformat()

        self.assertEqual(response, _DATE_FORMAT_RE)

    def test_get_paginator_class(self):
        """The default implementation of _get_paginator_class should return djangos paginator"""
        # Test the default implementation returns the expected class
        self.assertEqual(self.index.get_paginator_class(), Paginator)

        # Test the overridden implementation returns the expected class
        self.index.paginator_class = Mock()
        self.assertEqual(
            self.index.get_paginator_class(),
            self.index.paginator_class
        )

    def test_get_paginator(self):
        """The _get_paginator method should return a paginator instance"""
        object_list = ['foo', 'bar', 'baz']
        paginator = self.index.get_paginator(object_list, 1)
        self.assertIsInstance(paginator, Paginator)
        self.assertEqual(paginator.object_list, object_list)
        self.assertEqual(3, paginator.num_pages)

    def test_paginate_queryset(self):
        """paginate_queryset should return page and paginator."""
        self.request.is_preview = True
        children = self.index._get_children(self.request)
        page, paginator = self.index.paginate_queryset(children['items'], 1)

        self.assertIsInstance(page, PaginatorPage)
        self.assertIsInstance(paginator, Paginator)
        self.assertEqual(paginator.per_page, self.index.paginate_by)
        self.assertEqual(paginator.num_pages, 1)

    @patch(
        'wagtail_events.abstract_models.AbstractPaginatedIndex.get_paginator_kwargs',
        Mock(return_value={'foo': 'bar'})
    )
    @patch('wagtail_events.abstract_models.AbstractPaginatedIndex.get_paginator')
    def test_paginate_queryset_calls_get_paginator(self, get_paginator):
        """paginate_queryset should call the get_paginator method."""
        self.request.is_preview = True
        children = self.index._get_children(self.request)
        self.index.paginate_queryset(children, 1)
        get_paginator.assert_called_with(children, self.index.paginate_by, foo='bar')

    def test_pagination(self):
        """Test EventIndex.get_context paginates correctly."""
        factories.EventOccurrenceFactory.create(
            event=self.detail,
            start_date=timezone.now(),
        )
        self.index.paginate_by = 1
        self.index.save()
        response = self.index.get_context(self.request)

        self.assertIsInstance(response['paginator'], Paginator)
        self.assertTrue(response['is_paginated'])
        self.assertIn(self.instance, response['children']['items'].object_list)

    def test_show_in_menus(self):
        """ Should take in account child.show_in_menus """
        request = RequestFactory().get('')
        request.is_preview = True
        self.index.paginate_by = 10
        self.index.save()
        context = self.index.get_context(request)
        self.assertIn(self.instance, context['children']['items'].object_list)
        self.assertNotIn(self.instance_2, context['children']['items'].object_list)


class TestEventOccurrence(TestCase):
    """Tests for the EventOccurrence model."""
    def setUp(self):
        self.model = models.EventOccurrence

    def test_parent_class(self):
        """The EventOccurrence model should inhert from AbstractEventOccurrence."""
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractEventOccurrence
        ))

    def test_body(self):
        """Test the EventOccurrence.body field."""
        field = self.model._meta.get_field('body')

        self.assertIsInstance(field, RichTextField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_event(self):
        """Test the EventOccurrence.event relationship."""
        field = self.model._meta.get_field('event')

        self.assertIsInstance(field, ParentalKey)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_url(self):
        """Test the EventOccurrence.url method return the correct data."""
        index = factories.EventIndexFactory.create(parent=None)
        SiteFactory.create(root_page=index)
        detail = factories.EventDetailFactory.create(parent=index)
        instance = factories.EventOccurrenceFactory.create(
            event=detail,
            start_date=timezone.now(),
        )
        self.assertEqual(instance.url, '{}{}/'.format(detail.url, instance.pk))

    def test_clean(self):
        """Clean should raise a validation error when end_date is before the start_date."""
        now = timezone.now()
        instance = models.EventOccurrence(
                event=factories.EventDetailFactory.create(parent=None),
                start_date=now,
                end_date=now-timedelta(minutes=1),
        )
        with self.assertRaises(ValidationError):
            instance.clean()
