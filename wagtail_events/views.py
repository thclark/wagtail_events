from django.views.generic import DetailView

from wagtail_events.models import SubEvent


class SubEventDetailView(DetailView):
    """SubEvent detail view."""
    model = SubEvent
