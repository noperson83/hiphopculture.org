from django.contrib import admin

from schedule.forms import EventAdminForm
from schedule.models import Calendar, CalendarRelation, Event, Occurrence, Rule


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': [
                ('name', 'slug'),
            ]
        }),
    )


@admin.register(CalendarRelation)
class CalendarRelationAdmin(admin.ModelAdmin):
    list_display = ('calendar', 'content_object')
    list_filter = ('inheritable',)
    fieldsets = (
        (None, {
            'fields': [
                'calendar',
                ('content_type', 'object_id', 'distinction',),
                'inheritable',
            ]
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end')
    list_filter = ('start',)
    ordering = ('-start',)
    date_hierarchy = 'start'
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': [
                ('title', 'color_event'),
                ('project', 'lead', 'artist', 'start_time', 'text', 'equip', 'details'),
                ('description',),
                ('start', 'end'),
                ('creator', 'calendar'),
                ('rule', 'end_recurring_period'),
            ]
        }),
    )
    form = EventAdminForm


admin.site.register(Occurrence, admin.ModelAdmin)


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('frequency',)
    search_fields = ('name', 'description')
