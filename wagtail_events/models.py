import datetime
import re

from django.db.models import CharField
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import CharBlock, TextBlock, BlockQuoteBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock

from wagtail_events import abstract_models as abstracts
from wagtail_events import date_filters
from wagtail_events import utils


class EventSeries(RoutablePageMixin, Page):

    body = StreamField([
        ('heading', CharBlock(required=False, label='Event / Event Series description subheading', max_length=120, help_text="Add optional subheadings between paragraphs, if you're describing the event in more detail")),
        ('paragraph', TextBlock(required=False, label='Event / Event Series description text', help_text='Tell people about the event or event series')),
        ('image', ImageChooserBlock(required=False, label='Event / Event Series Image(s)', help_text='Add images to describe the event or event series.')),
    ], blank=True, help_text='Add a description of this event or event series.')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('sub_events', label='Event Date(s)'),
    ]

    @route(r'(?P<pk>\d+)/$', name='event_detail')
    def event_view(self, request, *args, **kwargs):
        from wagtail_events.views import SubEventDetailView
        return SubEventDetailView.as_view()(request, *args, **kwargs)

    parent_page_types = ['wagtail_events.EventIndex']
    subpage_types = []


class SubEvent(abstracts.AbstractSubEvent):

    body = StreamField([
        ('heading', CharBlock(required=False, label='Sub-event description subheading', max_length=120, help_text="Add optional subheadings between paragraphs, if you're describing the event in more detail")),
        ('paragraph', TextBlock(required=False, label='Sub-event description text', help_text='Tell people about the event')),
        ('image', ImageChooserBlock(required=False, label='Sub-event image', help_text='Add images to the event.')),
        ('quote', BlockQuoteBlock(required=False, help_text='Add an inspirational quote!')),
        ], blank=True, help_text='Optional information specific to this particular event date')

    event_series = ParentalKey(EventSeries, related_name='sub_events', help_text='The main event or event series')

    @property
    def url(self):
        """Returns the full url of the object."""
        url = self.event_series.reverse_subpage('event_detail', kwargs={'pk': self.pk})
        return self.event_series.url + url

    panels = abstracts.AbstractSubEvent.panels + [
        StreamFieldPanel('body'),
    ]


class EventIndex(abstracts.AbstractEventIndex):

    body = StreamField([
        ('paragraph', TextBlock(required=False, label='Events page text', help_text='Tell people about what kind of events you run')),
        ('quote', BlockQuoteBlock(required=False, help_text='Add an inspirational quote!')),
    ], blank=True, help_text='Specify what people see when they reach the events page')

    content_panels = abstracts.AbstractPaginatedIndex.content_panels + [
        StreamFieldPanel('body'),
    ]

    def _get_children(self, request):
        """
        Gets the SubEvents related to the EventSeries

        :param request: django request
        :return: Queryset of child model instances
        """
        qs = super(EventIndex, self)._get_children(request)

        default_period = 'day'
        time_periods = {
            'year': date_filters.get_year_agenda,
            'week': date_filters.get_week_agenda,
            'month': date_filters.get_month_agenda,
            default_period: date_filters.get_day_agenda,
        }
        period = request.GET.get('scope', default_period).lower()

        if period not in time_periods.keys():
            return {'items': SubEvent.objects.filter(event_series__in=qs)}

        start_date = request.GET.get('start_date', '')
        if re.match(self.get_dateformat(), start_date):
            date_params = [int(i) for i in start_date.split('.')]
            start_date = utils.date_to_datetime(datetime.date(*date_params))
        else:
            start_date = timezone.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

        return time_periods[period](SubEvent, qs, start_date)

    subpage_types = ['wagtail_events.EventSeries']
