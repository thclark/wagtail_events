# -*- coding:utf8 -*-

from __future__ import unicode_literals

import factory

from wagtail_factories import PageFactory

from wagtail_events import models


class EventDetailFactory(PageFactory):
    """Factory for wagtail_events.models.EventDetail"""
    title = factory.Sequence('Event {}'.format)
    body = factory.Sequence('Event {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventDetail


class EventIndexFactory(PageFactory):
    """Factory for wagtail_events.models.EventIndex"""
    title = factory.Sequence('Event List {}'.format)
    body = factory.Sequence('Event List {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventIndex


class EventOccurrenceFactory(factory.django.DjangoModelFactory):
    """Factory for wagtail_events.models.EventOccurrence"""
    title = factory.Sequence('Event instance {}'.format)
    body = factory.Sequence('Event instance {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventOccurrence
