from django.contrib import admin
from .models import TaskModel

@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ('taskTitle', 'taskDescription', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('taskTitle', 'taskDescription')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(is_completed=True)
    mark_as_completed.short_description = "Mark selected tasks as completed"
