from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailEventsAppConfig(AppConfig):
    name = 'wagtail_events'
    label = 'wagtail_events'
    verbose_name = _('Wagtail Events')
