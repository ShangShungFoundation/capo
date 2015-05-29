from django.contrib import admin
from models import Recipe, Task, Job, Log
from django_admin_bootstrapped.admin.models import SortableInline


class TaskInline(admin.StackedInline, SortableInline):
    model = Task
    extra = 0


class LogInline(admin.StackedInline):
    model = Log
    extra = 0


class JobAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'id', 'status', 'execute_after', 'submited_by', 'submited_at')
    list_filter = ('status', 'submited_by',)
    readonly_fields = ("started_at", "completed_at", "submited_by")
    save_as = True

    inlines = [
        LogInline,
    ]

    fieldsets = (
        (None, {
            'fields': (
                "recipe",
                "param",
                ("submited_by"),
                "observations",
            )
        }),
        ('On failure', {
            'fields': (
                "on_failure",
                "on_failure_param",
            )
        }),
        ('Result', {
            'fields': (
                ("started_at", "completed_at"),
                "result",
            )
        }),
    )


    def save_model(self, request, obj, form, change):
        if getattr(obj, 'submited_by', None) is None:
            obj.submited_by = request.user
        obj.save()


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by",)
    save_as = True

    inlines = [
        TaskInline,
    ]

    fieldsets = (
        (None, {
            'fields': (
                ("name", "label"),
                "max_jobs",
                "param",
                "description",
                "created_by"
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


class TaskAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (
                "recipe",
                "is_active",
            )
        }),
        ('Action', {
            'fields': (
                "action_name",
                "param",
            )
        }),
        ('On Failure', {
            'fields': (
                "on_error_action",
                "on_error_param",
            )
        }),
    )


class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'code', 'job', 'msg', )
    list_filter = ('code', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Log, LogAdmin)
