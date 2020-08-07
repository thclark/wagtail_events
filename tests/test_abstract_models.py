from django.db import models
from django.test import TestCase
from wagtail.core.models import Page

from wagtail_events import abstract_models


class TestAbstractPaginatedIndex(TestCase):
    """Tests for the AbstractPaginatedIndex model."""

    def setUp(self):
        self.model = abstract_models.AbstractPaginatedIndex

    def test_parent_class(self):
        """AbstractPaginatedIndex shoild inhert from Page."""
        self.assertTrue(issubclass(self.model, Page))

    def test_paginate_by(self):
        """Test AbstractPaginatedIndex.paginate_by field type."""
        field = self.model._meta.get_field("paginate_by")
        self.assertIsInstance(field, models.PositiveIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)


class TestAbstractEventIndex(TestCase):
    """Tests for the AbstractEventIndex model."""

    def test_parent_class(self):
        """The model should inhert from page & AbstractPaginatedIndex."""
        self.assertTrue(issubclass(abstract_models.AbstractEventIndex, abstract_models.AbstractPaginatedIndex))
