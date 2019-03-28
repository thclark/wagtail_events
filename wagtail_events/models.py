from django.db import models
from django.urls import reverse
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import CharBlock, TextBlock, BlockQuoteBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


from wagtail_events.abstract_models import AbstractEvent, AbstractEventIndex


def get_image_model_path():
    from django.conf import settings
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


class Event(RoutablePageMixin, AbstractEvent):

    image = models.ForeignKey(get_image_model_path(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    description = models.TextField(max_length=400, help_text='Briefly describe your event series', null=False, blank=True)
    body = StreamField([
        ('heading', CharBlock(required=False, label='Optional extra description subheading', max_length=120, help_text="Add optional subheadings between paragraphs, if you're describing the event series in more detail")),
        ('paragraph', TextBlock(required=False, label='Optional extra description text', help_text='Tell people about the event series')),
        ('image', ImageChooserBlock(required=False, label='Optional extra event series image(s)', help_text='Add images to describe the event series.')),
        ('quote', BlockQuoteBlock(required=False, help_text='Add an inspirational quote!')),
    ], blank=True, help_text='Add a description of this event or event series.')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('description'),
                ImageChooserPanel('image'),
            ],
            heading="Event Series Description"
        )] + AbstractEvent.content_panels + [
        StreamFieldPanel('body', heading='Extra Information')
    ]

    parent_page_types = ['wagtail_events.EventIndex']
    subpage_types = []

    @route(r'(?P<pk>\d+)/$', name='event_detail')
    def event_view(self, request, *args, **kwargs):
        from wagtail_events.views import EventDetailView
        return EventDetailView.as_view()(request, *args, **kwargs)

    @property
    def url(self):
        """Returns the full url of the object."""
        url = reverse('event_detail', kwargs={'pk': self.pk})
        return url


class EventIndex(RoutablePageMixin, AbstractEventIndex):
    pass
