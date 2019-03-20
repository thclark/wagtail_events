import factory

from wagtail_factories import PageFactory

from wagtail_events import models


# TODO have the factories synthesize non-blank streamfields


class EventSeriesFactory(PageFactory):
    """Factory for wagtail_events.models.EventSeries"""
    title = factory.Sequence('EventSeries {}'.format)
    # body = factory.Sequence('EventSeries {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventSeries


class EventIndexFactory(PageFactory):
    """Factory for wagtail_events.models.EventIndex"""
    title = factory.Sequence('Event Index {}'.format)
    # body = factory.Sequence('Event Index {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventIndex


class SubEventFactory(factory.django.DjangoModelFactory):
    """Factory for wagtail_events.models.SubEvent"""
    title = factory.Sequence('SubEvent instance {}'.format)
    # body = factory.Sequence('SubEvent instance {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.SubEvent
