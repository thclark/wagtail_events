from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import CharBlock, TextBlock, BlockQuoteBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


from wagtail_events.abstract_models import AbstractEvent, AbstractEventIndex


def get_image_model_path():
    from django.conf import settings
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


class Event(AbstractEvent):

    image = models.ForeignKey(get_image_model_path(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    description = models.TextField(max_length=400, help_text='Briefly describe your event', null=False, blank=True)
    body = StreamField([
        ('heading', CharBlock(required=False, label='Subheading', max_length=120, help_text="Add optional subheadings between paragraphs, if you're describing the event series in more detail")),
        ('paragraph', TextBlock(required=False, label='Text', help_text='Tell people about the event series')),
        ('image', ImageChooserBlock(required=False, label='Image', help_text='Add images to describe the event series.')),
        ('quote', BlockQuoteBlock(required=False, label='Quote', help_text='Add an inspirational quote!')),
    ], blank=True, help_text='Optional: Add further description of this event.')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('description'),
                ImageChooserPanel('image'),
            ],
            heading="Event Description"
        )] + AbstractEvent.content_panels + [
        StreamFieldPanel('body', heading='Extra Information')
    ]

    parent_page_types = ['wagtail_events.EventIndex']
    subpage_types = []


class EventIndex(AbstractEventIndex):
    subpage_types = ['wagtail_events.Event']
