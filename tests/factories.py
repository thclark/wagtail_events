import factory

from wagtail_factories import PageFactory

from wagtail_events import models


# TODO have the factories synthesize non-blank streamfields


class EventFactory(PageFactory):
    """Factory for wagtail_events.models.EventSeries"""
    title = factory.Sequence('Event {}'.format)
    # body = factory.Sequence('Event {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.Event


class EventIndexFactory(PageFactory):
    """Factory for wagtail_events.models.EventIndex"""
    title = factory.Sequence('Event Index {}'.format)
    # body = factory.Sequence('Event Index {} information.'.format)

    class Meta(object):
        """Factory properties."""
        model = models.EventIndex
