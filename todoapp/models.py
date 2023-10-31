from django.db import models

class TaskModel(models.Model):
    taskTitle = models.CharField(max_length=100)
    taskDescription = models.TextField()
    is_completed = models.BooleanField(default=False)
    taskDueDate = models.DateField(null=True, blank=True)
    taskPriority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])

    def __str__(self):
        return self.taskTitle
