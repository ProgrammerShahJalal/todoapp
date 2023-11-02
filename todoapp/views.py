from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files import File
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
import pytz
from .models import TaskModel, Photo
from .forms import TaskForm, TaskFilterForm



def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()

            for image in request.FILES.getlist('images'):
                photo = Photo(image=image)
                photo.save()
                task.images.add(photo)

            return redirect('show_tasks')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})




def edit_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    user_timezone = request.session.get('user_timezone', 'UTC')  # Retrieve the user's time zone

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            # Delete existing images
            for image in task.images.all():
                # Delete image file from the storage
                default_storage.delete(image.image.name)
                # Delete the Photo object
                image.delete()

            # Add the new images
            for image in request.FILES.getlist('images'):
                photo = Photo(image=image)
                photo.save()
                task.images.add(photo)

            task = form.save()
            return redirect('show_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task, 'user_timezone': user_timezone})





def show_tasks(request):
    user_timezone = request.session.get('user_timezone', 'UTC')  # Retrieve the user's time zone

    title = request.GET.get('title')
    created_at = request.GET.get('created_at')
    priority = request.GET.get('priority')
    is_completed = request.GET.get('is_completed')
    due_date = request.GET.get('due_date')

    tasks = TaskModel.objects.all()

    if title:
        tasks = tasks.filter(taskTitle__icontains=title)

    if created_at:
        # Parse the date string and convert to user's timezone
        created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        created_at = pytz.timezone('UTC').localize(datetime(created_at.year, created_at.month, created_at.day))
        created_at = created_at.astimezone(pytz.timezone(user_timezone))
        # Filter tasks based on the date
        tasks = tasks.filter(created_at__date=created_at)

    if priority:
        tasks = tasks.filter(taskPriority=priority)

    if is_completed:
        tasks = tasks.filter(is_completed=is_completed == 'true')

    if due_date:
        # Parse the date string and convert to the user's timezone
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        due_date = pytz.timezone('UTC').localize(due_date)
        due_date = due_date.astimezone(pytz.timezone(user_timezone))
    
        # Calculate the date range for filtering tasks
        start_date = due_date.replace(hour=0, minute=0, second=0)
        end_date = due_date.replace(hour=23, minute=59, second=59)
    
        # Filter tasks with due dates that fall within the date range
        tasks = tasks.filter(taskDueDate__gte=start_date, taskDueDate__lte=end_date)


        # Check if the "Clear All" button was clicked
    if 'clear_all' in request.GET:
        return redirect('show_tasks')


    return render(request, 'show_tasks.html', {'tasks': tasks, 'user_timezone': user_timezone})





def complete_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.is_completed = True
    task.save()
    return redirect('completed_tasks')

def delete_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.delete()
    return redirect('show_tasks')

def completed_tasks(request):
    tasks = TaskModel.objects.filter(is_completed=True)
    return render(request, 'completed_tasks.html', {'tasks': tasks})

def completed_task_delete(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.delete()
    return redirect('completed_tasks')
