from django.contrib import admin
from wagtail_events.models import EventIndex, Event


admin.site.register(Event)
admin.site.register(EventIndex)
