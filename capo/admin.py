from django.contrib import admin
from models import Recipe, Task, Job, Log, Worker, WorkerCapacity
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
    save_as = True
    inlines = [LogInline]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'submited_by', None) is None:
            obj.submited_by = request.user
        obj.save()


class RecipeAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
    save_as = True


class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'code', 'job', 'msg', )
    list_filter = ('code', )


class LogInline(admin.StackedInline):
    model = Log
    extra = 0


class WorkerCapacityInline(admin.StackedInline):
    model = WorkerCapacity
    extra = 0


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'communication', 'active', )
    inlines = [WorkerCapacityInline]
    save_as = True


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(Job, JobAdmin)
admin.site.register(Log, LogAdmin)
