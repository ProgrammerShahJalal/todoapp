from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    taskTitle = models.CharField(max_length=100)
    taskDescription = models.TextField()
    is_completed = models.BooleanField(default=False)
    taskDueDate = models.DateTimeField(default=timezone.now)
    taskPriority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    images = models.ManyToManyField('Photo', related_name='tasks', blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # Use timezone.now to set the current timestamp
    updated_at = models.DateTimeField(auto_now=True)  # This field will automatically update on every save

    def delete(self, *args, **kwargs):
        # Delete associated images when a task is deleted
        for image in self.images.all():
            image.image.delete()
            image.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.taskTitle

class Photo(models.Model):
    image = models.ImageField(upload_to='todoapp/static/todoapp')

    def __str__(self):
        return str(self.image)
