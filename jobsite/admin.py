from django.contrib import admin

from .models import Jobsite

@admin.register(Jobsite)
class JobsiteAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_summary', 'city')
    