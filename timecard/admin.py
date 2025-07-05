from django.contrib import admin
from .models import TimeCard
import copy  # (1) use python copy

def copy_time_card(modeladmin, request, queryset):
    # tc is an instance of SemesterDetails
    for tc in queryset:
        tc_copy = copy.copy(tc) # (2) django copy object
        tc_copy.id = None   # (3) set 'id' to None to create new object
        tc_copy.save()    # initial save

        # zero out enrollment numbers.  
        # (6) Use __dict__ to access "regular" attributes (not FK or M2M)
        for attr_name in ['date', 'artist', 'project', 'site_time', 'site_end_time', 'site_time_after', 'site_end_time_after']:
            tc_copy.__dict__.update({ attr_name : 0})
 
        tc_copy.save()  # (7) save the copy to the database for M2M relations

    copy_time_card.short_description = "Make a Copy of Time Card"

class TimeCardAdmin(admin.ModelAdmin):
    actions = [copy_time_card]   #  HERE IT IS!
    save_on_top = True
    list_display = ('id', 'date', 'artist', 'project', 'site_time', 'site_end_time', 'site_time_after', 'site_end_time_after', 'day_total') 
    list_filter = ('date', 'artist', 'project')     
    date_hierarchy = 'date'
    search_fields = ('date', 'artist', 'project')
    
admin.site.register(TimeCard, TimeCardAdmin)

