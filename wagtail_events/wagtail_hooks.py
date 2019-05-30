from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.site_summary import SummaryItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks
from wagtail_events.models import Event


class EventsSummaryItem(SummaryItem):
    order = 300
    template = 'wagtail_events/homepage/site_summary_events.html'

    def get_context(self):
        return {
            'total_events': Event.objects.count(),
        }


@hooks.register('construct_homepage_summary_items')
def add_homepage_summary_item(request, items):
    items.append(EventsSummaryItem(request))


class EventModelAdmin(ModelAdmin):

    model = Event

    menu_icon = 'date'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'description',)
    list_filter = ('title', )
    search_fields = ('title', 'description',)

    # Editor panels configuration
    content_panels = [
        FieldPanel('title'),
    ]


modeladmin_register(EventModelAdmin)

