from django.contrib import admin
from .models import ArtistProfile, Group

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'group', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'group')
    search_fields = ('email', 'first_name', 'last_name', 'group__name')
    ordering = ('first_name', 'last_name')
    fieldsets = (
        ("Personal Information", {
            "fields": ("email", "first_name", "last_name", "bio", "profile_pic", "cover_photo", "website")
        }),
        ("Contact & Social Media", {
            "fields": ("phone_number", "facebook_url", "instagram_url", "twitter_url", "youtube_url", "spotify_url")
        }),
        ("Music Details", {
            "fields": ("group", )
        }),
        ("Permissions & Access", {
            "fields": ("is_active", "is_staff", "is_admin", "has_calendar_access", "has_task_management")
        }),
        ("Time Tracking", {
            "fields": ("total_hours_logged", "last_clock_in", "last_clock_out")
        }),
    )






