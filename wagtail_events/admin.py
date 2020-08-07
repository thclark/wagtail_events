from django.contrib import admin
from wagtail_events.models import Event, EventIndex


admin.site.register(Event)
admin.site.register(EventIndex)
