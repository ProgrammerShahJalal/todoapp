from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from todoapp.views import add_task, show_tasks, task_details, update_task, forbidden_task, complete_task, delete_task, completed_tasks, completed_task_delete, user_register, user_login, user_logout

urlpatterns = [
    path('', show_tasks, name='show_tasks'),
    path('show_tasks/', show_tasks, name='show_tasks'),
    path('add_task/', add_task, name='add_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('task/<int:task_id>/', task_details, name='task_details'),
    path('task/<int:task_id>/update/', update_task, name='update_task'),
    path('forbidden_task/', forbidden_task, name='forbidden_task'),
    path('completed_tasks/', completed_tasks, name='completed_tasks'),
    path('completed_task_delete/<int:task_id>/', completed_task_delete, name='completed_task_delete'),
    
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
