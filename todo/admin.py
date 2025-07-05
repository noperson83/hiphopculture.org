from django.contrib import admin
from todo.models import Task, TaskList, Comment
from project.models import ScopeOfWork, Device, Wire, Hardware, Software

class TaskInline(admin.TabularInline):
    model = Task

class TaskListAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "scope", 'priority')
    list_filter = ("scope",)
    list_select_related = ('scope',)
    inlines = [TaskInline]
    list_editable = 'group', 'scope', 'priority',
    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs['request']
        formfield = super(TaskListAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'scope':
            choices = getattr(request, '_myfield_choices_cache', None)
            if choices is None:
                request._myfield_choices_cache = choices = list(formfield.choices)
            formfield.choices = choices
        return formfield

class DeviceInline(admin.TabularInline):
    model = Device
class WireInline(admin.TabularInline):
    model = Wire
class HardwareInline(admin.TabularInline):
    model = Hardware
class SoftwareInline(admin.TabularInline):
    model = Software

class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ("title", "allotted_time", "get_project", "task_list", "completed", "priority", "due_date")
    list_filter = ("task_list",)
    ordering = ("priority",)
    search_fields = ("name",)
    list_editable = 'priority',
    inlines = [DeviceInline, WireInline, HardwareInline, SoftwareInline]
    
    def get_project(self, obj):
        return obj.task_list.scope.project
    get_project.short_description = 'Project'

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "date", "snippet")

admin.site.register(TaskList, TaskListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)




