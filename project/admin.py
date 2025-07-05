from django.contrib import admin

from .models import Project, ScopeOfWork, Device, Wire, Hardware, Software, License, Travel
from todo.models import TaskList
import copy  # (1) use python copy

class TaskListInline(admin.TabularInline):
    model = TaskList

@admin.register(ScopeOfWork)
class ScopeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('project',
                    'area', 
                    'system_type',
                    'priority',
                    'dateofcreation',
                    'lastmodification')
    list_filter = ('project',
                    'area', 
                    'system_type',
                    'dateofcreation',
                    'lastmodification')
    readonly_fields = ['dateofcreation']
    search_fields = ('area',)
    ordering =     ('project',
                    'area', 
                    'system_type',
                    'priority',)
    list_editable = 'priority',
    date_hierarchy = 'dateofcreation'
    inlines = [TaskListInline]

def copy_project(modeladmin, request, queryset):
    # sd is an instance of a project
    for sd in queryset:
        sd_copy = copy.copy(sd) # (2) django copy object
        sd_copy.pk = None   # (3) set 'id' to None to create new object
        sd_copy.save()    # initial save

        for lead in sd.lead.all():
            sd_copy.lead.add(lead)

        for workers in sd.workers.all():
            sd_copy.workers.add(workers)
 
    sd_copy.save()  # (7) save the copy to the database for M2M relations

copy_project.short_description = "Make a Copy of a Project"
def make_job_status_i(modeladmin, request, queryset):
    queryset.update(job_status='i')
make_job_status_i.short_description = "Mark selected projects as Invoiced"
def make_job_status_m(modeladmin, request, queryset):
    queryset.update(job_status='m')
make_job_status_m.short_description = "Mark selected projects as Paid"
def make_job_status_l(modeladmin, request, queryset):
    queryset.update(job_status='l')
make_job_status_l.short_description = "Mark selected projects as Lost/Cancelled"
def make_job_status_o(modeladmin, request, queryset):
    queryset.update(job_status='o')
make_job_status_o.short_description = "Mark selected projects as Installing"
def make_job_status_c(modeladmin, request, queryset):
    queryset.update(job_status='c')
make_job_status_c.short_description = "Mark selected projects as Complete"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_requested'
    list_display = ('job_num', 
                    'job_name',
                    'revision', 
                    'jobsite',
                    'projectmanager',
                    'estimator', 
                    'date_requested', 
                    'job_status', 
                    'due_date', 
                    'paid_date')
    list_editable = 'job_name', 'job_status'
    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs['request']
        formfield = super(ProjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'job_status':
            choices = getattr(request, '_myfield_choices_cache', None)
            if choices is None:
                request._myfield_choices_cache = choices = list(formfield.choices)
            formfield.choices = choices
        return formfield
    actions = [make_job_status_i, make_job_status_m, make_job_status_l, make_job_status_o, make_job_status_c]

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device', 'project', 'task', 'qty', 'cost', 'total', 'purchased_date', 'onsite_date', 'installed_date', 'dateofcreation', 'lastmodification')

admin.site.register(Device, DeviceAdmin)

class WireAdmin(admin.ModelAdmin):
    list_display = ('wire', 'project', 'task', 'length', 'cost_per_foot', 'total', 'purchased_date', 'onsite_date', 'installed_date', 'dateofcreation', 'lastmodification')

admin.site.register(Wire, WireAdmin)

class HardwareAdmin(admin.ModelAdmin):
    list_display = ('hardware', 'project', 'task', 'qty', 'cost', 'total', 'purchased_date', 'onsite_date', 'installed_date', 'dateofcreation', 'lastmodification')

admin.site.register(Hardware, HardwareAdmin)

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('software', 'project', 'task', 'qty', 'cost', 'total', 'purchased_date', 'onsite_date', 'installed_date', 'dateofcreation', 'lastmodification')

admin.site.register(Software, SoftwareAdmin)

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license', 'project', 'task', 'qty', 'cost', 'total', 'purchased_date', 'onsite_date', 'installed_date', 'dateofcreation', 'lastmodification')

admin.site.register(License, LicenseAdmin)

class TravelAdmin(admin.ModelAdmin):
    list_display = ('project', 'task', 'travel_name', 'hotel_name', 'cost', 'total', 'gas_estimate', 'dateofcreation', 'lastmodification')

admin.site.register(Travel, TravelAdmin)