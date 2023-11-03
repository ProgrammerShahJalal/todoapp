from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.core.files import File
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
import pytz
from .models import TaskModel, Photo
from .forms import TaskForm, TaskFilterForm




""" ================ AUTHENTICATION START ============== """

# user register
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login') 
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

# user login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request = request, data = request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = username, password = password)

                if user is not None:
                    login(request, user)
                    return redirect('show_tasks')
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        return redirect('show_tasks')

def user_logout(request):
    logout(request)

    return redirect('login')




""" ================ AUTHENTICATION END ============== """

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)  # Create a task object without saving to the database
            task.user = request.user  # Set the user for the task
            task.save()  # Save the task with the associated user

            for image in request.FILES.getlist('images'):
                photo = Photo(image=image)
                photo.save()
                task.images.add(photo)

            return redirect('show_tasks')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})



@login_required
def show_tasks(request):
    user_timezone = request.session.get('user_timezone', 'UTC')  # Retrieve the user's time zone

    title = request.GET.get('title')
    created_at = request.GET.get('created_at')
    priority = request.GET.get('priority')
    is_completed = request.GET.get('is_completed')
    due_date = request.GET.get('due_date')

    tasks = TaskModel.objects.filter(user=request.user)

    if title:
        tasks = tasks.filter(taskTitle__icontains=title)

    if created_at:
        # Parse the date string and convert to user's timezone
        created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        created_at = pytz.timezone('UTC').localize(datetime(created_at.year, created_at.month, created_at.day))
        created_at = created_at.astimezone(pytz.timezone(user_timezone))
        # Filter tasks based on the date
        tasks = tasks.filter(created_at__date=created_at)
        tasks = tasks.filter(created_at__range=(created_at_start, created_at_end))

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




@login_required
def task_details(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id, user=request.user)


    return render(request, 'task_details.html', {'task': task})




@login_required
def update_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    
    # Check if the task is completed
    if task.is_completed:
        # If the task is completed, return a custom response with CSS and a "Go Back" button
        return render(request, 'forbidden_task.html')
    
    user_timezone = request.session.get('user_timezone', 'UTC')

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            # Delete existing images
            for image in task.images.all():
                default_storage.delete(image.image.name)
                image.delete()

            # Add the new images
            for image in request.FILES.getlist('new_images'):
                photo = Photo(image=image)
                photo.save()
                task.images.add(photo)

            task = form.save()
            return redirect('show_tasks')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'update_task.html', {'form': form, 'task': task, 'user_timezone': user_timezone})



@login_required
def complete_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.is_completed = True
    task.save()
    return redirect('completed_tasks')

@login_required
def delete_task(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.delete()
    return redirect('show_tasks')

@login_required
def completed_tasks(request):
    tasks = TaskModel.objects.filter(is_completed=True, user=request.user)
    return render(request, 'completed_tasks.html', {'tasks': tasks})

@login_required
def completed_task_delete(request, task_id):
    task = TaskModel.objects.get(pk=task_id)
    task.delete()
    return redirect('completed_tasks')




def forbidden_task(request):
    return render(request, 'forbidden_task.html')