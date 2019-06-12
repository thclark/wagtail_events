import datetime
import re
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils import timezone
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page

from wagtail_events import date_filters
from wagtail_events.managers import DatedEventManager
from wagtail_events import utils
from wagtail_events.utils import _DATE_FORMAT_RE


class AbstractPaginatedIndex(Page):
    """ """
    paginate_by = models.PositiveIntegerField(blank=True, null=True)
    content_panels = Page.content_panels + [FieldPanel('paginate_by')]
    paginator_class = Paginator

    class Meta(object):
        """Django model meta options."""
        abstract = True

    def _get_children(self, request, *args, **kwargs):
        """
        Helper method for getting child nodes to display in the listing.

        :param request: django request
        :return: Queryset of child model instances
        """
        model_class = self.__class__.allowed_subpage_models()[0]
        children = model_class.objects.child_of(self)
        if not request.is_preview:
            children = children.filter(live=True)

        # Children should only be displayed if show_in_menus is true.
        children = children.filter(show_in_menus=True)

        return children

    def get_paginator_class(self):
        """
        Returns the class to use for pagination

        :return: Paginator class
        """
        return self.paginator_class

    def get_paginator_kwargs(self):
        """
        Method for generating a dict of keyword args that will be
        passed to the paginator constructor

        :param request: HttpRequest instance
        :return: Dict of keyword arguments to pass to the paginator class constructor
        """
        return {}

    def get_paginator(self, *args, **kwargs):
        """
        Returns a paginator instance

        :return: Paginator class
        """
        paginator_class = self.get_paginator_class()
        return paginator_class(*args, **kwargs)

    def paginate_queryset(self, queryset, page):
        """
        Helper method for paginating the queryset provided.

        :param queryset: Queryset of model instances to paginate
        :param page: Raw page number taken from the request dict
        :return: Queryset of child model instances
        """
        paginator = self.get_paginator(
            queryset,
            self.paginate_by,
            **self.get_paginator_kwargs()
        )
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return queryset, paginator

    def get_context(self, request, *args, **kwargs):
        """
        Adds child pages to the context and paginates them.

        :param request: HttpRequest instance
        :param args: default positional args
        :param kwargs: default keyword args
        :return: Context data to use when rendering the template
        """
        context = super(AbstractPaginatedIndex, self).get_context(
            request,
            *args,
            **kwargs
        )
        queryset = self._get_children(request, *args, **kwargs)
        is_paginated = False
        paginator = None

        # Paginate the child nodes if paginate_by has been specified
        if self.paginate_by:
            is_paginated = True
            page_num = request.GET.get('page', 1) or 1
            queryset['items'], paginator = self.paginate_queryset(
                queryset['items'],
                page_num
            )

        context.update(
            children=queryset,
            paginator=paginator,
            is_paginated=is_paginated
        )
        return context


class AbstractEventIndex(AbstractPaginatedIndex):

    class Meta(object):
        abstract = True

    def get_dateformat(self):
        """
        Returns the date format regex
        """
        return _DATE_FORMAT_RE

    def _get_children(self, request, *args, **kwargs):
        """
        :param request: django request
        :return: Queryset of child model instances, filtered by a scope and start date in the request params
        """
        qs = super(AbstractEventIndex, self)._get_children(request).specific()

        time_periods = {
            'year': date_filters.get_year_range,
            'week': date_filters.get_week_range,
            'month': date_filters.get_month_range,
            'day': date_filters.get_day_range,
        }
        period = request.GET.get('scope', None)

        if period:

            # Get the start date from the request (or use default now)
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

            # Clean the start and end dates to conform to the requested period
            start_date, end_date = time_periods[period.lower()](start_date)

            # Filter the original queryset to the date range specified
            qs.filter(start_date__gte=start_date).filter(end_date__lte=end_date)

        return qs


class AbstractEvent(Page):

    start_date = models.DateTimeField(help_text='Event start time')
    end_date = models.DateTimeField(blank=True, null=True, help_text='Event end time')
    event_website = models.URLField(blank=True, null=True, help_text='Optional external link for the event or programme')
    venue = models.TextField(blank=True, null=True, help_text='The event venue')
    venue_website = models.URLField(blank=True, null=True, help_text='Link to the venue (or, say, a google maps pin)')
    objects = DatedEventManager()

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('end_date'),
                FieldPanel('event_website'),
            ],
            heading="Event Details"
        ),
        MultiFieldPanel(
            [
                FieldPanel('venue'),
                FieldPanel('venue_website'),
            ],
            heading="Venue Details"
        ),
    ]

    parent_page_types = ['wagtail_events.EventIndex']
    subpage_types = []

    class Meta(object):
        abstract = True
        ordering = ['start_date']

    def clean(self):
        """Clean the model fields, if end_date is before start_date raise a ValidationError."""
        super(AbstractEvent, self).clean()
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'The end date cannot be before the start date.'})
