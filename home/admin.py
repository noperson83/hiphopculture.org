from django.contrib import admin
from .models import SiteSettings
from .models import Subscriber

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for managing site-wide settings."""
    list_display = ('promotion_message', 'active_trend')  # Fields to display in the admin list
    list_editable = ('active_trend',)  # Only fields other than the first can be editable
    list_display_links = ('promotion_message',)  # Explicitly set a link for the first field
    fieldsets = (
        (None, {
            'fields': ('promotion_message', 'active_trend'),
            'description': 'Update the global promotion message and the active trend for the site.',
        }),
    )

class SubscriberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {
            'fields': ['email'],
        }),
    ]
    list_display = ('email', 'date_subscribed')  # This will show 'date_subscribed' in the list view

admin.site.register(Subscriber, SubscriberAdmin)