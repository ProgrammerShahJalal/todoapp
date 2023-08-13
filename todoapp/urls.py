from django.urls import path
from todoapp.views import add_task, show_tasks, edit_task, complete_task, delete_task

urlpatterns = [
    path('', show_tasks, name='show_tasks'),
    path('show_tasks/', show_tasks, name='show_tasks'),
    path('add_task/', add_task, name='add_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    # path('completed_tasks/', completed_tasks, name='completed_tasks'),
]
