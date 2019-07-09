from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailEventsAppConfig(AppConfig):
    name = 'wagtail_references'
    label = 'wagtail_references'
    verbose_name = _('Wagtail References')
