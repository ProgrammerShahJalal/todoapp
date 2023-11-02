from django.shortcuts import render, redirect
from .models import TaskModel, Photo
from .forms import TaskForm

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
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save()

            # Remove existing images and add the new ones
            task.images.clear()
            for image in request.FILES.getlist('images'):
                photo = Photo(image=image)
                photo.save()
                task.images.add(photo)

            return redirect('show_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


def show_tasks(request):
    tasks = TaskModel.objects.filter(is_completed=False)
    return render(request, 'show_tasks.html', {'tasks': tasks})

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
