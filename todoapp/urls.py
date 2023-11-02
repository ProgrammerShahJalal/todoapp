from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from todoapp.views import add_task, show_tasks, edit_task, complete_task, delete_task, completed_tasks, completed_task_delete

urlpatterns = [
    path('', show_tasks, name='show_tasks'),
    path('show_tasks/', show_tasks, name='show_tasks'),
    path('add_task/', add_task, name='add_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('completed_tasks/', completed_tasks, name='completed_tasks'),
    path('completed_task_delete/<int:task_id>/', completed_task_delete, name='completed_task_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

