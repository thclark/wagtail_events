# -*- coding:utf8 -*-
"""omni_wagtail_events abstract models"""

from __future__ import unicode_literals

from django.views.generic import DetailView

from wagtail_events.models import EventOccurrence


class EventOccurrenceDetailView(DetailView):
    """EventOccurrence detail view."""
    model = EventOccurrence
